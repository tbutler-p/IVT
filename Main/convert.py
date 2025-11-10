"""Docling PDF-to-DocTags converter CLI.

This module exposes a configurable command-line interface around Docling's PDF
conversion pipeline. It demonstrates how to map every public configuration knob
onto argparse flags so that future developers can reason about the options by
reading a single file.

Key configuration surfaces:

* OCR engines (``auto``, ``rapidocr``, ``easyocr``, ``tesseract``, ``tesserocr``,
  ``ocrmac``) via the corresponding ``docling.datamodel.pipeline_options`` models.
* Table structure inference tuned through ``TableFormerMode`` which accepts
  ``fast`` or ``accurate``.
* Accelerator settings controlled through ``AcceleratorDevice`` values
  (``auto``, ``cpu``, ``cuda``, ``mps``) and thread counts.
* Layout model presets such as ``docling_layout_heron`` or
  ``docling_layout_v2`` defined in ``docling.datamodel.layout_model_specs``.
* Output formats backed by ``docling.datamodel.base_models.OutputFormat``.

All options are applied explicitly—even when left at their default values—to
make the effective configuration self-documenting. The script logs its work to
``Main/convert.log`` with timestamps and per-run summaries of every knob.
"""

from __future__ import annotations

import argparse
import json
import logging
import platform
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.backend_options import PdfBackendOptions
from docling.datamodel.base_models import InputFormat, OutputFormat
from docling.datamodel.layout_model_specs import (
    DOCLING_LAYOUT_EGRET_LARGE,
    DOCLING_LAYOUT_EGRET_MEDIUM,
    DOCLING_LAYOUT_EGRET_XLARGE,
    DOCLING_LAYOUT_HERON,
    DOCLING_LAYOUT_HERON_101,
    DOCLING_LAYOUT_V2,
    LayoutModelConfig,
)
from docling.datamodel.pipeline_options import (
    LayoutOptions,
    OcrAutoOptions,
    OcrMacOptions,
    OcrOptions,
    PdfPipelineOptions,
    PictureDescriptionBaseOptions,
    PictureDescriptionVlmOptions,
    RapidOcrOptions,
    TableFormerMode,
    TableStructureOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
    granite_picture_description,
    smolvlm_picture_description,
)
from docling.datamodel.pipeline_options import EasyOcrOptions
from docling.datamodel.settings import DEFAULT_PAGE_RANGE
from docling.document_converter import DocumentConverter, PdfFormatOption

BASE_DIR = Path(__file__).resolve().parent


def parse_bool(value: str) -> bool:
    """Parse a string into a boolean value.

    Args:
        value: Input string such as ``"true"``, ``"false"``, ``"yes"``, or ``"no"``.

    Returns:
        Parsed boolean.

    Raises:
        argparse.ArgumentTypeError: If the input does not map to a boolean.
    """

    normalized = value.strip().lower()
    if normalized in {"true", "t", "1", "yes", "y"}:
        return True
    if normalized in {"false", "f", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"Cannot interpret '{value}' as boolean.")


def parse_optional_bool(value: str) -> Optional[bool]:
    """Parse a string into an optional boolean.

    Args:
        value: Input string. ``"none"`` (case-insensitive) maps to ``None``.

    Returns:
        ``True``, ``False``, or ``None``.

    Raises:
        argparse.ArgumentTypeError: If the input does not map to a valid option.
    """

    if value.strip().lower() == "none":
        return None
    return parse_bool(value)


def parse_page_range(expression: str) -> Tuple[int, int]:
    """Parse a page range expression in ``start:end`` form.

    Args:
        expression: String containing exactly one ``:`` delimiter.

    Returns:
        Tuple ``(start, end)`` inclusive.

    Raises:
        argparse.ArgumentTypeError: If the expression is malformed.
    """

    parts = expression.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"Page range '{expression}' must use the form <start>:<end>."
        )
    try:
        start = int(parts[0])
        end = int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Page range values must be integers: {expression}"
        ) from exc
    if start <= 0 or end <= 0 or start > end:
        raise argparse.ArgumentTypeError(
            f"Invalid page range '{expression}'. Ensure start <= end and both > 0."
        )
    return start, end


def configure_logging(log_path: Path) -> logging.Logger:
    """Configure logging to emit both file and console output.

    Args:
        log_path: Destination for the log file.

    Returns:
        Configured root logger.
    """

    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def list_supported_options() -> None:
    """Print all enum-driven configuration options to stdout."""

    table_modes = ", ".join(mode.value for mode in TableFormerMode)
    accelerator_devices = ", ".join(device.value for device in AcceleratorDevice)
    layout_models = ", ".join(
        [
            "docling_layout_v2",
            "docling_layout_heron",
            "docling_layout_heron_101",
            "docling_layout_egret_medium",
            "docling_layout_egret_large",
            "docling_layout_egret_xlarge",
        ]
    )
    ocr_variants = ", ".join(
        [
            "auto",
            "rapidocr",
            "easyocr",
            "tesseract",
            "tesserocr",
            "ocrmac",
        ]
    )
    output_formats = ", ".join(fmt.value for fmt in OutputFormat)
    backends = ", ".join(["docling_parse_v4", "pypdfium2"])

    print("Docling converter supported options")
    print("------------------------------------")
    print(f"TableFormerMode choices: {table_modes}")
    print(f"Accelerator devices: {accelerator_devices}")
    print(f"Layout models: {layout_models}")
    print(f"OCR engines: {ocr_variants}")
    print(f"PDF backends: {backends}")
    print(f"Output formats: {output_formats}")


LAYOUT_MODEL_MAP: Dict[str, LayoutModelConfig] = {
    "docling_layout_v2": DOCLING_LAYOUT_V2,
    "docling_layout_heron": DOCLING_LAYOUT_HERON,
    "docling_layout_heron_101": DOCLING_LAYOUT_HERON_101,
    "docling_layout_egret_medium": DOCLING_LAYOUT_EGRET_MEDIUM,
    "docling_layout_egret_large": DOCLING_LAYOUT_EGRET_LARGE,
    "docling_layout_egret_xlarge": DOCLING_LAYOUT_EGRET_XLARGE,
}

PDF_BACKEND_MAP = {
    "docling_parse_v4": DoclingParseV4DocumentBackend,
    "pypdfium2": PyPdfiumDocumentBackend,
}

OCR_ENGINE_MAP = {
    "auto": OcrAutoOptions,
    "rapidocr": RapidOcrOptions,
    "easyocr": EasyOcrOptions,
    "tesseract": TesseractCliOcrOptions,
    "tesserocr": TesseractOcrOptions,
    "ocrmac": OcrMacOptions,
}

PICTURE_DESCRIPTION_MAP = {
    "smolvlm": smolvlm_picture_description,
    "granite": granite_picture_description,
}


def resolve_output_formats(selected: Iterable[str]) -> List[OutputFormat]:
    """Convert CLI arguments into OutputFormat values.

    Args:
        selected: Sequence of format identifiers.

    Returns:
        List of unique ``OutputFormat`` members.

    Raises:
        argparse.ArgumentTypeError: If an unknown format is requested.
    """

    resolved: List[OutputFormat] = []
    seen: set[OutputFormat] = set()
    for value in selected:
        try:
            candidate = OutputFormat(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Unsupported output format '{value}'."
            ) from exc
        if candidate not in seen:
            resolved.append(candidate)
            seen.add(candidate)
    return resolved


def build_ocr_options(args: argparse.Namespace) -> OcrOptions:
    """Instantiate the OCR configuration requested on the command line.

    Valid engine identifiers:

    * ``auto`` -> :class:`docling.datamodel.pipeline_options.OcrAutoOptions`
    * ``rapidocr`` -> :class:`docling.datamodel.pipeline_options.RapidOcrOptions`
    * ``easyocr`` -> :class:`docling.datamodel.pipeline_options.EasyOcrOptions`
    * ``tesseract`` -> :class:`docling.datamodel.pipeline_options.TesseractCliOcrOptions`
    * ``tesserocr`` -> :class:`docling.datamodel.pipeline_options.TesseractOcrOptions`
    * ``ocrmac`` -> :class:`docling.datamodel.pipeline_options.OcrMacOptions`

    Args:
        args: Parsed CLI arguments.

    Returns:
        Concrete ``OcrOptions`` instance matching the selected engine.
    """

    lang = args.ocr_lang or []
    base_kwargs = {
        "lang": lang,
        "force_full_page_ocr": args.ocr_force_full_page,
        "bitmap_area_threshold": args.ocr_bitmap_area_threshold,
    }

    engine = args.ocr_engine
    if engine == "auto":
        return OcrAutoOptions(**base_kwargs)
    if engine == "rapidocr":
        return RapidOcrOptions(
            **base_kwargs,
            backend=args.rapidocr_backend,
            text_score=args.rapidocr_text_score,
            use_det=args.rapidocr_use_det,
            use_cls=args.rapidocr_use_cls,
            use_rec=args.rapidocr_use_rec,
            print_verbose=args.rapidocr_print_verbose,
            det_model_path=args.rapidocr_det_model_path,
            cls_model_path=args.rapidocr_cls_model_path,
            rec_model_path=args.rapidocr_rec_model_path,
            rec_keys_path=args.rapidocr_rec_keys_path,
            rec_font_path=args.rapidocr_rec_font_path,
            font_path=args.rapidocr_font_path,
            rapidocr_params={},
        )
    if engine == "easyocr":
        return EasyOcrOptions(
            **base_kwargs,
            use_gpu=args.easyocr_use_gpu,
            confidence_threshold=args.easyocr_confidence_threshold,
            model_storage_directory=args.easyocr_model_storage_directory,
            recog_network=args.easyocr_recog_network,
            download_enabled=args.easyocr_download_enabled,
            suppress_mps_warnings=args.easyocr_suppress_mps_warnings,
        )
    if engine == "tesseract":
        return TesseractCliOcrOptions(
            **base_kwargs,
            tesseract_cmd=args.tesseract_cli_cmd,
            path=args.tesseract_cli_path,
            psm=args.tesseract_cli_psm,
        )
    if engine == "tesserocr":
        return TesseractOcrOptions(
            **base_kwargs,
            path=args.tesserocr_path,
            psm=args.tesserocr_psm,
        )
    if engine == "ocrmac":
        return OcrMacOptions(
            **base_kwargs,
            recognition=args.ocrmac_recognition,
            framework=args.ocrmac_framework,
        )
    raise ValueError(f"Unsupported OCR engine '{engine}'.")


def build_picture_description_options(args: argparse.Namespace) -> PictureDescriptionBaseOptions:
    """Choose the picture description configuration block.

    Args:
        args: Parsed CLI arguments.

    Returns:
        A clone of the selected picture description profile with overrides applied.
    """

    if args.picture_description_profile in PICTURE_DESCRIPTION_MAP:
        base = PICTURE_DESCRIPTION_MAP[args.picture_description_profile]
        options = PictureDescriptionVlmOptions(
            repo_id=base.repo_id,
            prompt=base.prompt,
            generation_config=dict(base.generation_config),
        )
    else:
        options = PictureDescriptionBaseOptions()
    options.batch_size = args.picture_description_batch_size
    options.scale = args.picture_description_scale
    options.picture_area_threshold = args.picture_description_area_threshold
    return options


def build_pipeline_options(args: argparse.Namespace) -> PdfPipelineOptions:
    """Construct a fully-populated ``PdfPipelineOptions`` instance.

    Enumerated options combined in this structure:

    * ``TableFormerMode`` for ``--table-mode`` (``fast`` or ``accurate``).
    * ``AcceleratorDevice`` via ``--accelerator-device`` (``auto``, ``cpu``,
      ``cuda``, ``mps``).
    * Layout models derived from ``docling.datamodel.layout_model_specs``.
    * OCR engines resolved through :mod:`docling.datamodel.pipeline_options`.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Pipeline options ready to feed into ``PdfFormatOption``.
    """

    accelerator = AcceleratorOptions(
        num_threads=args.accelerator_num_threads,
        device=args.accelerator_device,
        cuda_use_flash_attention2=args.accelerator_use_flash_attention2,
    )

    table_structure = TableStructureOptions(
        do_cell_matching=args.table_do_cell_matching,
        mode=TableFormerMode(args.table_mode),
    )

    layout_options = LayoutOptions(
        create_orphan_clusters=args.layout_create_orphan_clusters,
        keep_empty_clusters=args.layout_keep_empty_clusters,
        model_spec=LAYOUT_MODEL_MAP[args.layout_model],
        skip_cell_assignment=args.layout_skip_cell_assignment,
    )

    picture_description_options = build_picture_description_options(args)
    ocr_options = build_ocr_options(args)

    return PdfPipelineOptions(
        document_timeout=args.document_timeout,
        accelerator_options=accelerator,
        enable_remote_services=args.enable_remote_services,
        allow_external_plugins=args.allow_external_plugins,
        artifacts_path=str(args.artifacts_path) if args.artifacts_path else None,
        do_picture_classification=args.do_picture_classification,
        do_picture_description=args.do_picture_description,
        picture_description_options=picture_description_options,
        images_scale=args.images_scale,
        generate_page_images=args.generate_page_images,
        generate_picture_images=args.generate_picture_images,
        do_table_structure=args.do_table_structure,
        do_ocr=args.do_ocr,
        do_code_enrichment=args.do_code_enrichment,
        do_formula_enrichment=args.do_formula_enrichment,
        force_backend_text=args.force_backend_text,
        table_structure_options=table_structure,
        ocr_options=ocr_options,
        layout_options=layout_options,
        generate_table_images=args.generate_table_images,
        generate_parsed_pages=args.generate_parsed_pages,
        ocr_batch_size=args.ocr_batch_size,
        layout_batch_size=args.layout_batch_size,
        table_batch_size=args.table_batch_size,
        batch_polling_interval_seconds=args.batch_polling_interval,
        queue_max_size=args.queue_max_size,
    )


def build_pdf_backend_options(args: argparse.Namespace) -> PdfBackendOptions:
    """Instantiate ``PdfBackendOptions`` from CLI inputs."""

    return PdfBackendOptions(
        enable_remote_fetch=args.pdf_enable_remote_fetch,
        enable_local_fetch=args.pdf_enable_local_fetch,
        password=args.pdf_password,
    )


def summarise_accelerator(device_value: str) -> str:
    """Return a human-readable accelerator description for logging."""

    device_lower = str(device_value).lower()
    if device_lower == "auto":
        system = platform.system().lower()
        machine = platform.machine().lower()
        if system == "darwin" and "arm" in machine:
            return "auto (Apple Silicon detected; Docling expected to pick MPS/MLX)."
        if system == "linux":
            return "auto (Linux host; Docling will prefer CUDA if available, else CPU)."
        return "auto (Docling will choose the optimal accelerator at runtime)."
    if device_lower.startswith("cuda"):
        return f"CUDA device requested ({device_lower})."
    if device_lower == "mps":
        return "Metal Performance Shaders (Apple Silicon) requested explicitly."
    if device_lower == "cpu":
        return "CPU inference requested explicitly."
    return f"Custom accelerator string requested: {device_value}"


def export_conversion_results(
    conversion_result,
    formats: Sequence[OutputFormat],
    output_dir: Path,
    stem: str,
    logger: logging.Logger,
) -> None:
    """Persist conversion outputs for the requested formats.

    Args:
        conversion_result: Docling ``ConversionResult`` instance.
        formats: Iterable of output formats to produce.
        output_dir: Destination directory.
        stem: Base filename (without suffix).
        logger: Application logger.
    """

    document = conversion_result.document
    exporters = {
        OutputFormat.DOCTAGS: (
            lambda: document.export_to_doctags(),
            ".doctags.txt",
        ),
        OutputFormat.TEXT: (lambda: document.export_to_text(), ".txt"),
        OutputFormat.MARKDOWN: (lambda: document.export_to_markdown(), ".md"),
        OutputFormat.JSON: (
            lambda: json.dumps(document.export_to_dict(), indent=2),
            ".json",
        ),
        OutputFormat.HTML: (lambda: document.export_to_html(), ".html"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        if fmt not in exporters:
            logger.warning("Skipping unsupported exporter for format %s.", fmt.value)
            continue
        producer, suffix = exporters[fmt]
        payload = producer()
        destination = output_dir / f"{stem}{suffix}"
        destination.write_text(payload, encoding="utf-8")
        logger.info("Wrote %s output to %s", fmt.value, destination)


def convert_documents(
    args: argparse.Namespace,
    pipeline_options: PdfPipelineOptions,
    backend_options: PdfBackendOptions,
    backend_key: str,
    output_formats: Sequence[OutputFormat],
    logger: logging.Logger,
) -> int:
    """Run the Docling conversion loop.

    Args:
        args: Parsed CLI arguments.
        pipeline_options: Fully configured pipeline options.
        backend_options: PDF backend configuration.
        backend_key: Key identifying the backend class.
        output_formats: Sequence of formats to emit.
        logger: Application logger.

    Returns:
        Number of failed conversions.
    """

    backend_cls = PDF_BACKEND_MAP[backend_key]
    converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=backend_cls,
                backend_options=backend_options,
            )
        },
    )

    pdf_files = sorted(
        path
        for path in args.input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )
    if not pdf_files:
        logger.warning("No PDF files found in %s.", args.input_dir)
        return 0

    page_range = (
        parse_page_range(args.page_range) if args.page_range else DEFAULT_PAGE_RANGE
    )
    max_num_pages = args.max_pages if args.max_pages is not None else sys.maxsize
    max_file_size = args.max_file_size if args.max_file_size is not None else sys.maxsize

    failures = 0
    for pdf_path in pdf_files:
        logger.info("Starting conversion: %s", pdf_path)
        try:
            result = converter.convert(
                source=pdf_path,
                raises_on_error=args.raises_on_error,
                max_num_pages=max_num_pages,
                max_file_size=max_file_size,
                page_range=page_range,
            )
        except Exception as exc:  # noqa: BLE001 -- surface full exception detail
            failures += 1
            logger.exception("Conversion failed for %s: %s", pdf_path, exc)
            continue

        output_base = args.output_dir
        stem = pdf_path.stem
        export_conversion_results(result, output_formats, output_base, stem, logger)

        page_count = len(result.pages) if result.pages else 0
        logger.info(
            "Completed %s | status=%s | pages=%d",
            pdf_path,
            result.status.value if hasattr(result.status, "value") else result.status,
            page_count,
        )
    return failures


def log_configuration(
    logger: logging.Logger,
    args: argparse.Namespace,
    pipeline_options: PdfPipelineOptions,
    backend_options: PdfBackendOptions,
    output_formats: Sequence[OutputFormat],
) -> None:
    """Emit a detailed configuration summary to the log."""

    logger.info("Input directory: %s", args.input_dir)
    logger.info("Output directory: %s", args.output_dir)
    logger.info("Requested output formats: %s", [fmt.value for fmt in output_formats])
    logger.info("PDF backend: %s", args.pdf_backend)
    logger.info("OCR engine: %s", args.ocr_engine)
    logger.info("Accelerator: %s", summarise_accelerator(pipeline_options.accelerator_options.device))
    logger.info(
        "Pipeline options snapshot: %s",
        pipeline_options.model_dump(mode="python"),
    )
    logger.info(
        "PDF backend options snapshot: %s",
        backend_options.model_dump(mode="python"),
    )
    logger.info(
        "Conversion parameters: {raises_on_error=%s, max_pages=%s, max_file_size=%s, page_range=%s}",
        args.raises_on_error,
        args.max_pages,
        args.max_file_size,
        args.page_range,
    )


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Set up argparse with every surfaced Docling configuration knob.

    The most important enum-driven flags are summarised below:

    * ``--table-mode`` accepts values from :class:`TableFormerMode`.
    * ``--ocr-engine`` accepts values from ``OCR_ENGINE_MAP``.
    * ``--layout-model`` accepts keys from ``LAYOUT_MODEL_MAP``.
    * ``--accelerator-device`` accepts values from :class:`AcceleratorDevice`.
    * ``--output-formats`` accepts :class:`OutputFormat` values.
    * ``--pdf-backend`` accepts keys from ``PDF_BACKEND_MAP``.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Convert PDFs in Main/input to DocTags and other formats using Docling. "
            "All pipeline options are exposed as CLI flags; defaults mirror Docling's "
            "published defaults so the configuration is fully self-documenting."
        )
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=BASE_DIR / "input",
        help="Directory containing source PDFs (default: Main/input).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BASE_DIR / "output" / "doctags",
        help="Destination directory for generated outputs.",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=BASE_DIR / "convert.log",
        help="Log file path; the file is truncated at the start of each run.",
    )
    parser.add_argument(
        "--list-options",
        action="store_true",
        help="List available enums (OCR engines, table modes, etc.) and exit.",
    )

    parser.add_argument(
        "--output-formats",
        nargs="+",
        default=[OutputFormat.DOCTAGS.value],
        help="One or more output formats using OutputFormat enum values.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Hard cap on pages processed per document (None for unlimited).",
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=None,
        help="Reject files larger than this many bytes (None disables the check).",
    )
    parser.add_argument(
        "--raises-on-error",
        type=parse_bool,
        default=False,
        help="If true, Docling will raise on conversion errors instead of continuing.",
    )
    parser.add_argument(
        "--page-range",
        type=str,
        default=None,
        help="Optional page range in the form start:end (1-indexed, inclusive).",
    )

    parser.add_argument(
        "--document-timeout",
        type=float,
        default=None,
        help="Optional timeout (seconds) applied to pipeline stages.",
    )
    parser.add_argument(
        "--enable-remote-services",
        type=parse_bool,
        default=False,
        help="Allow pipelines to call remote services (default: false).",
    )
    parser.add_argument(
        "--allow-external-plugins",
        type=parse_bool,
        default=False,
        help="Enable dynamic plugin loading (default: false).",
    )
    parser.add_argument(
        "--artifacts-path",
        type=Path,
        default=None,
        help="Optional path where Docling stores cached artifacts.",
    )

    parser.add_argument(
        "--do-picture-classification",
        type=parse_bool,
        default=False,
        help="Toggle picture classification stage.",
    )
    parser.add_argument(
        "--do-picture-description",
        type=parse_bool,
        default=False,
        help="Toggle picture description stage.",
    )
    parser.add_argument(
        "--picture-description-profile",
        choices=list(PICTURE_DESCRIPTION_MAP.keys()) + ["base"],
        default="smolvlm",
        help="Select the base picture description preset.",
    )
    parser.add_argument(
        "--picture-description-batch-size",
        type=int,
        default=8,
        help="Batch size for picture description models.",
    )
    parser.add_argument(
        "--picture-description-scale",
        type=float,
        default=2.0,
        help="Resize factor for picture description crops.",
    )
    parser.add_argument(
        "--picture-description-area-threshold",
        type=float,
        default=0.05,
        help="Minimum picture area ratio required to trigger description.",
    )

    parser.add_argument(
        "--images-scale",
        type=float,
        default=1.0,
        help="Scale factor for generated page images.",
    )
    parser.add_argument(
        "--generate-page-images",
        type=parse_bool,
        default=False,
        help="Produce rendered page images alongside structured output.",
    )
    parser.add_argument(
        "--generate-picture-images",
        type=parse_bool,
        default=False,
        help="Persist extracted picture crops.",
    )
    parser.add_argument(
        "--generate-table-images",
        type=parse_bool,
        default=False,
        help="Deprecated flag retained for completeness; kept for visibility.",
    )
    parser.add_argument(
        "--generate-parsed-pages",
        type=parse_bool,
        default=False,
        help="If true, intermediate parsed page data is stored.",
    )

    parser.add_argument(
        "--do-table-structure",
        type=parse_bool,
        default=True,
        help="Enable table structure inference.",
    )
    parser.add_argument(
        "--do-ocr",
        type=parse_bool,
        default=True,
        help="Enable OCR processing.",
    )
    parser.add_argument(
        "--do-code-enrichment",
        type=parse_bool,
        default=False,
        help="Enable code-specific OCR enrichment routines.",
    )
    parser.add_argument(
        "--do-formula-enrichment",
        type=parse_bool,
        default=False,
        help="Enable formula OCR enrichment.",
    )
    parser.add_argument(
        "--force-backend-text",
        type=parse_bool,
        default=False,
        help="Force Docling to use backend text instead of OCR output.",
    )
    parser.add_argument(
        "--table-mode",
        choices=[mode.value for mode in TableFormerMode],
        default=TableFormerMode.ACCURATE.value,
        help="TableFormer operating mode.",
    )
    parser.add_argument(
        "--table-do-cell-matching",
        type=parse_bool,
        default=True,
        help="Whether to reconcile model output with PDF cell structure.",
    )

    parser.add_argument(
        "--ocr-engine",
        choices=list(OCR_ENGINE_MAP.keys()),
        default="auto",
        help="OCR engine selection.",
    )
    parser.add_argument(
        "--ocr-lang",
        nargs="+",
        default=["en"],
        help="Languages supplied to the OCR engine (use ISO codes).",
    )
    parser.add_argument(
        "--ocr-force-full-page",
        type=parse_bool,
        default=False,
        help="Always run full-page OCR regardless of heuristics.",
    )
    parser.add_argument(
        "--ocr-bitmap-area-threshold",
        type=float,
        default=0.05,
        help="Minimum bitmap area ratio that triggers OCR.",
    )

    parser.add_argument(
        "--rapidocr-backend",
        choices=["onnxruntime", "openvino", "paddle", "torch"],
        default="onnxruntime",
    )
    parser.add_argument(
        "--rapidocr-text-score",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--rapidocr-use-det",
        type=parse_optional_bool,
        default=None,
    )
    parser.add_argument(
        "--rapidocr-use-cls",
        type=parse_optional_bool,
        default=None,
    )
    parser.add_argument(
        "--rapidocr-use-rec",
        type=parse_optional_bool,
        default=None,
    )
    parser.add_argument(
        "--rapidocr-print-verbose",
        type=parse_bool,
        default=False,
    )
    parser.add_argument("--rapidocr-det-model-path", default=None)
    parser.add_argument("--rapidocr-cls-model-path", default=None)
    parser.add_argument("--rapidocr-rec-model-path", default=None)
    parser.add_argument("--rapidocr-rec-keys-path", default=None)
    parser.add_argument("--rapidocr-rec-font-path", default=None)
    parser.add_argument("--rapidocr-font-path", default=None)

    parser.add_argument(
        "--easyocr-use-gpu",
        type=parse_optional_bool,
        default=None,
    )
    parser.add_argument(
        "--easyocr-confidence-threshold",
        type=float,
        default=0.5,
    )
    parser.add_argument("--easyocr-model-storage-directory", default=None)
    parser.add_argument("--easyocr-recog-network", default="standard")
    parser.add_argument(
        "--easyocr-download-enabled",
        type=parse_bool,
        default=True,
    )
    parser.add_argument(
        "--easyocr-suppress-mps-warnings",
        type=parse_bool,
        default=True,
    )

    parser.add_argument("--tesseract-cli-cmd", default="tesseract")
    parser.add_argument("--tesseract-cli-path", default=None)
    parser.add_argument("--tesseract-cli-psm", type=int, default=None)
    parser.add_argument("--tesserocr-path", default=None)
    parser.add_argument("--tesserocr-psm", type=int, default=None)
    parser.add_argument("--ocrmac-recognition", default="accurate")
    parser.add_argument("--ocrmac-framework", default="vision")

    parser.add_argument(
        "--layout-create-orphan-clusters",
        type=parse_bool,
        default=True,
    )
    parser.add_argument(
        "--layout-keep-empty-clusters",
        type=parse_bool,
        default=False,
    )
    parser.add_argument(
        "--layout-skip-cell-assignment",
        type=parse_bool,
        default=False,
    )
    parser.add_argument(
        "--layout-model",
        choices=list(LAYOUT_MODEL_MAP.keys()),
        default="docling_layout_heron",
    )

    parser.add_argument(
        "--ocr-batch-size",
        type=int,
        default=4,
    )
    parser.add_argument(
        "--layout-batch-size",
        type=int,
        default=4,
    )
    parser.add_argument(
        "--table-batch-size",
        type=int,
        default=4,
    )
    parser.add_argument(
        "--batch-polling-interval",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--queue-max-size",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--accelerator-device",
        choices=[device.value for device in AcceleratorDevice],
        default=AcceleratorDevice.AUTO.value,
    )
    parser.add_argument(
        "--accelerator-num-threads",
        type=int,
        default=4,
    )
    parser.add_argument(
        "--accelerator-use-flash-attention2",
        type=parse_bool,
        default=False,
    )

    parser.add_argument(
        "--pdf-backend",
        choices=list(PDF_BACKEND_MAP.keys()),
        default="docling_parse_v4",
    )
    parser.add_argument(
        "--pdf-enable-remote-fetch",
        type=parse_bool,
        default=False,
    )
    parser.add_argument(
        "--pdf-enable-local-fetch",
        type=parse_bool,
        default=False,
    )
    parser.add_argument("--pdf-password", default=None)

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Application entry point."""

    args = parse_arguments(argv)
    if args.list_options:
        list_supported_options()
        return 0

    args.input_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    logger = configure_logging(args.log_path)
    logger.info("Docling converter starting.")

    output_formats = resolve_output_formats(args.output_formats)
    pipeline_options = build_pipeline_options(args)
    backend_options = build_pdf_backend_options(args)

    log_configuration(logger, args, pipeline_options, backend_options, output_formats)

    failures = convert_documents(
        args=args,
        pipeline_options=pipeline_options,
        backend_options=backend_options,
        backend_key=args.pdf_backend,
        output_formats=output_formats,
        logger=logger,
    )

    if failures:
        logger.error("Conversion completed with %d failure(s).", failures)
        return 1

    logger.info("Conversion completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
