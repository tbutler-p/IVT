# Table of Contents

* [psutil](#psutil)
  * [Process](#psutil.Process)
    * [pid](#psutil.Process.pid)
    * [oneshot](#psutil.Process.oneshot)
    * [as\_dict](#psutil.Process.as_dict)
    * [parent](#psutil.Process.parent)
    * [parents](#psutil.Process.parents)
    * [is\_running](#psutil.Process.is_running)
    * [ppid](#psutil.Process.ppid)
    * [name](#psutil.Process.name)
    * [exe](#psutil.Process.exe)
    * [cmdline](#psutil.Process.cmdline)
    * [status](#psutil.Process.status)
    * [username](#psutil.Process.username)
    * [create\_time](#psutil.Process.create_time)
    * [cwd](#psutil.Process.cwd)
    * [nice](#psutil.Process.nice)
    * [num\_ctx\_switches](#psutil.Process.num_ctx_switches)
    * [num\_threads](#psutil.Process.num_threads)
    * [children](#psutil.Process.children)
    * [cpu\_percent](#psutil.Process.cpu_percent)
    * [cpu\_times](#psutil.Process.cpu_times)
    * [memory\_info](#psutil.Process.memory_info)
    * [memory\_full\_info](#psutil.Process.memory_full_info)
    * [memory\_percent](#psutil.Process.memory_percent)
    * [open\_files](#psutil.Process.open_files)
    * [net\_connections](#psutil.Process.net_connections)
    * [send\_signal](#psutil.Process.send_signal)
    * [suspend](#psutil.Process.suspend)
    * [resume](#psutil.Process.resume)
    * [terminate](#psutil.Process.terminate)
    * [kill](#psutil.Process.kill)
    * [wait](#psutil.Process.wait)
  * [Popen](#psutil.Popen)
  * [pids](#psutil.pids)
  * [pid\_exists](#psutil.pid_exists)
  * [process\_iter](#psutil.process_iter)
  * [wait\_procs](#psutil.wait_procs)
  * [cpu\_count](#psutil.cpu_count)
  * [cpu\_times](#psutil.cpu_times)
  * [cpu\_percent](#psutil.cpu_percent)
  * [cpu\_times\_percent](#psutil.cpu_times_percent)
  * [cpu\_stats](#psutil.cpu_stats)
  * [virtual\_memory](#psutil.virtual_memory)
  * [swap\_memory](#psutil.swap_memory)
  * [disk\_usage](#psutil.disk_usage)
  * [disk\_partitions](#psutil.disk_partitions)
  * [disk\_io\_counters](#psutil.disk_io_counters)
  * [net\_io\_counters](#psutil.net_io_counters)
  * [net\_connections](#psutil.net_connections)
  * [net\_if\_addrs](#psutil.net_if_addrs)
  * [net\_if\_stats](#psutil.net_if_stats)
  * [boot\_time](#psutil.boot_time)
  * [users](#psutil.users)

<a id="psutil"></a>

# psutil

psutil is a cross-platform library for retrieving information on
running processes and system utilization (CPU, memory, disks, network,
sensors) in Python. Supported platforms:

 - Linux
 - Windows
 - macOS
 - FreeBSD
 - OpenBSD
 - NetBSD
 - Sun Solaris
 - AIX

Supported Python versions are cPython 3.6+ and PyPy.

<a id="psutil.Process"></a>

## Process Objects

```python
class Process()
```

Represents an OS process with the given PID.
If PID is omitted current process PID (os.getpid()) is used.
Raise NoSuchProcess if PID does not exist.

Note that most of the methods of this class do not make sure that
the PID of the process being queried has been reused. That means
that you may end up retrieving information for another process.

The only exceptions for which process identity is pre-emptively
checked and guaranteed are:

 - parent()
 - children()
 - nice() (set)
 - ionice() (set)
 - rlimit() (set)
 - cpu_affinity (set)
 - suspend()
 - resume()
 - send_signal()
 - terminate()
 - kill()

To prevent this problem for all other methods you can use
is_running() before querying the process.

<a id="psutil.Process.pid"></a>

#### pid

```python
@property
def pid()
```

The process PID.

<a id="psutil.Process.oneshot"></a>

#### oneshot

```python
@contextlib.contextmanager
def oneshot()
```

Utility context manager which considerably speeds up the
retrieval of multiple process information at the same time.

Internally different process info (e.g. name, ppid, uids,
gids, ...) may be fetched by using the same routine, but
only one information is returned and the others are discarded.
When using this context manager the internal routine is
executed once (in the example below on name()) and the
other info are cached.

The cache is cleared when exiting the context manager block.
The advice is to use this every time you retrieve more than
one information about the process. If you're lucky, you'll
get a hell of a speedup.

>>> import psutil
>>> p = psutil.Process()
>>> with p.oneshot():
...     p.name()  # collect multiple info
...     p.cpu_times()  # return cached value
...     p.cpu_percent()  # return cached value
...     p.create_time()  # return cached value
...
>>>

<a id="psutil.Process.as_dict"></a>

#### as\_dict

```python
def as_dict(attrs=None, ad_value=None)
```

Utility method returning process information as a
hashable dictionary.
If *attrs* is specified it must be a list of strings
reflecting available Process class' attribute names
(e.g. ['cpu_times', 'name']) else all public (read
only) attributes are assumed.
*ad_value* is the value which gets assigned in case
AccessDenied or ZombieProcess exception is raised when
retrieving that particular process information.

<a id="psutil.Process.parent"></a>

#### parent

```python
def parent()
```

Return the parent process as a Process object pre-emptively
checking whether PID has been reused.
If no parent is known return None.

<a id="psutil.Process.parents"></a>

#### parents

```python
def parents()
```

Return the parents of this process as a list of Process
instances. If no parents are known return an empty list.

<a id="psutil.Process.is_running"></a>

#### is\_running

```python
def is_running()
```

Return whether this process is running.

It also checks if PID has been reused by another process, in
which case it will remove the process from `process_iter()`
internal cache and return False.

<a id="psutil.Process.ppid"></a>

#### ppid

```python
@memoize_when_activated
def ppid()
```

The process parent PID.
On Windows the return value is cached after first call.

<a id="psutil.Process.name"></a>

#### name

```python
def name()
```

The process name. The return value is cached after first call.

<a id="psutil.Process.exe"></a>

#### exe

```python
def exe()
```

The process executable as an absolute path.
May also be an empty string.
The return value is cached after first call.

<a id="psutil.Process.cmdline"></a>

#### cmdline

```python
def cmdline()
```

The command line this process has been called with.

<a id="psutil.Process.status"></a>

#### status

```python
def status()
```

The process current status as a STATUS_* constant.

<a id="psutil.Process.username"></a>

#### username

```python
def username()
```

The name of the user that owns the process.
On UNIX this is calculated by using *real* process uid.

<a id="psutil.Process.create_time"></a>

#### create\_time

```python
def create_time()
```

The process creation time as a floating point number
expressed in seconds since the epoch (seconds since January 1,
1970, at midnight UTC). The return value, which is cached after
first call, is based on the system clock, which means it may be
affected by changes such as manual adjustments or time
synchronization (e.g. NTP).

<a id="psutil.Process.cwd"></a>

#### cwd

```python
def cwd()
```

Process current working directory as an absolute path.

<a id="psutil.Process.nice"></a>

#### nice

```python
def nice(value=None)
```

Get or set process niceness (priority).

<a id="psutil.Process.num_ctx_switches"></a>

#### num\_ctx\_switches

```python
def num_ctx_switches()
```

Return the number of voluntary and involuntary context
switches performed by this process.

<a id="psutil.Process.num_threads"></a>

#### num\_threads

```python
def num_threads()
```

Return the number of threads used by this process.

<a id="psutil.Process.children"></a>

#### children

```python
def children(recursive=False)
```

Return the children of this process as a list of Process
instances, pre-emptively checking whether PID has been reused.
If *recursive* is True return all the parent descendants.

Example (A == this process):

 A ─┐
    │
    ├─ B (child) ─┐
    │             └─ X (grandchild) ─┐
    │                                └─ Y (great grandchild)
    ├─ C (child)
    └─ D (child)

>>> import psutil
>>> p = psutil.Process()
>>> p.children()
B, C, D
>>> p.children(recursive=True)
B, X, Y, C, D

Note that in the example above if process X disappears
process Y won't be listed as the reference to process A
is lost.

<a id="psutil.Process.cpu_percent"></a>

#### cpu\_percent

```python
def cpu_percent(interval=None)
```

Return a float representing the current process CPU
utilization as a percentage.

When *interval* is 0.0 or None (default) compares process times
to system CPU times elapsed since last call, returning
immediately (non-blocking). That means that the first time
this is called it will return a meaningful 0.0 value.

When *interval* is > 0.0 compares process times to system CPU
times elapsed before and after the interval (blocking).

In this case is recommended for accuracy that this function
be called with at least 0.1 seconds between calls.

A value > 100.0 can be returned in case of processes running
multiple threads on different CPU cores.

The returned value is explicitly NOT split evenly between
all available logical CPUs. This means that a busy loop process
running on a system with 2 logical CPUs will be reported as
having 100% CPU utilization instead of 50%.

**Examples**:

  
  >>> import psutil
  >>> p = psutil.Process(os.getpid())
  >>> # blocking
  >>> p.cpu_percent(interval=1)
  2.0
  >>> # non-blocking (percentage since last call)
  >>> p.cpu_percent(interval=None)
  2.9
  >>>

<a id="psutil.Process.cpu_times"></a>

#### cpu\_times

```python
@memoize_when_activated
def cpu_times()
```

Return a (user, system, children_user, children_system)
namedtuple representing the accumulated process time, in
seconds.
This is similar to os.times() but per-process.
On macOS and Windows children_user and children_system are
always set to 0.

<a id="psutil.Process.memory_info"></a>

#### memory\_info

```python
@memoize_when_activated
def memory_info()
```

Return a namedtuple with variable fields depending on the
platform, representing memory information about the process.

The "portable" fields available on all platforms are `rss` and `vms`.

All numbers are expressed in bytes.

<a id="psutil.Process.memory_full_info"></a>

#### memory\_full\_info

```python
def memory_full_info()
```

This method returns the same information as memory_info(),
plus, on some platform (Linux, macOS, Windows), also provides
additional metrics (USS, PSS and swap).
The additional metrics provide a better representation of actual
process memory usage.

Namely USS is the memory which is unique to a process and which
would be freed if the process was terminated right now.

It does so by passing through the whole process address.
As such it usually requires higher user privileges than
memory_info() and is considerably slower.

<a id="psutil.Process.memory_percent"></a>

#### memory\_percent

```python
def memory_percent(memtype="rss")
```

Compare process memory to total physical system memory and
calculate process memory utilization as a percentage.
*memtype* argument is a string that dictates what type of
process memory you want to compare against (defaults to "rss").
The list of available strings can be obtained like this:

>>> psutil.Process().memory_info()._fields
('rss', 'vms', 'shared', 'text', 'lib', 'data', 'dirty', 'uss', 'pss')

<a id="psutil.Process.open_files"></a>

#### open\_files

```python
def open_files()
```

Return files opened by process as a list of
(path, fd) namedtuples including the absolute file name
and file descriptor number.

<a id="psutil.Process.net_connections"></a>

#### net\_connections

```python
def net_connections(kind='inet')
```

Return socket connections opened by process as a list of
(fd, family, type, laddr, raddr, status) namedtuples.
The *kind* parameter filters for connections that match the
following criteria:

+------------+----------------------------------------------------+
| Kind Value | Connections using                                  |
+------------+----------------------------------------------------+
| inet       | IPv4 and IPv6                                      |
| inet4      | IPv4                                               |
| inet6      | IPv6                                               |
| tcp        | TCP                                                |
| tcp4       | TCP over IPv4                                      |
| tcp6       | TCP over IPv6                                      |
| udp        | UDP                                                |
| udp4       | UDP over IPv4                                      |
| udp6       | UDP over IPv6                                      |
| unix       | UNIX socket (both UDP and TCP protocols)           |
| all        | the sum of all the possible families and protocols |
+------------+----------------------------------------------------+

<a id="psutil.Process.send_signal"></a>

#### send\_signal

```python
def send_signal(sig)
```

Send a signal *sig* to process pre-emptively checking
whether PID has been reused (see signal module constants) .
On Windows only SIGTERM is valid and is treated as an alias
for kill().

<a id="psutil.Process.suspend"></a>

#### suspend

```python
def suspend()
```

Suspend process execution with SIGSTOP pre-emptively checking
whether PID has been reused.
On Windows this has the effect of suspending all process threads.

<a id="psutil.Process.resume"></a>

#### resume

```python
def resume()
```

Resume process execution with SIGCONT pre-emptively checking
whether PID has been reused.
On Windows this has the effect of resuming all process threads.

<a id="psutil.Process.terminate"></a>

#### terminate

```python
def terminate()
```

Terminate the process with SIGTERM pre-emptively checking
whether PID has been reused.
On Windows this is an alias for kill().

<a id="psutil.Process.kill"></a>

#### kill

```python
def kill()
```

Kill the current process with SIGKILL pre-emptively checking
whether PID has been reused.

<a id="psutil.Process.wait"></a>

#### wait

```python
def wait(timeout=None)
```

Wait for process to terminate and, if process is a children
of os.getpid(), also return its exit code, else None.
On Windows there's no such limitation (exit code is always
returned).

If the process is already terminated immediately return None
instead of raising NoSuchProcess.

If *timeout* (in seconds) is specified and process is still
alive raise TimeoutExpired.

To wait for multiple Process(es) use psutil.wait_procs().

<a id="psutil.Popen"></a>

## Popen Objects

```python
class Popen(Process)
```

Same as subprocess.Popen, but in addition it provides all
psutil.Process methods in a single class.
For the following methods which are common to both classes, psutil
implementation takes precedence:

* send_signal()
* terminate()
* kill()

This is done in order to avoid killing another process in case its
PID has been reused, fixing BPO-6973.

  >>> import psutil
  >>> from subprocess import PIPE
  >>> p = psutil.Popen(["python", "-c", "print 'hi'"], stdout=PIPE)
  >>> p.name()
  'python'
  >>> p.uids()
  user(real=1000, effective=1000, saved=1000)
  >>> p.username()
  'giampaolo'
  >>> p.communicate()
  ('hi', None)
  >>> p.terminate()
  >>> p.wait(timeout=2)
  0
  >>>

<a id="psutil.pids"></a>

#### pids

```python
def pids()
```

Return a list of current running PIDs.

<a id="psutil.pid_exists"></a>

#### pid\_exists

```python
def pid_exists(pid)
```

Return True if given PID exists in the current process list.
This is faster than doing "pid in psutil.pids()" and
should be preferred.

<a id="psutil.process_iter"></a>

#### process\_iter

```python
def process_iter(attrs=None, ad_value=None)
```

Return a generator yielding a Process instance for all
running processes.

Every new Process instance is only created once and then cached
into an internal table which is updated every time this is used.
Cache can optionally be cleared via `process_iter.cache_clear()`.

The sorting order in which processes are yielded is based on
their PIDs.

*attrs* and *ad_value* have the same meaning as in
Process.as_dict(). If *attrs* is specified as_dict() is called
and the resulting dict is stored as a 'info' attribute attached
to returned Process instance.
If *attrs* is an empty list it will retrieve all process info
(slow).

<a id="psutil.wait_procs"></a>

#### wait\_procs

```python
def wait_procs(procs, timeout=None, callback=None)
```

Convenience function which waits for a list of processes to
terminate.

Return a (gone, alive) tuple indicating which processes
are gone and which ones are still alive.

The gone ones will have a new *returncode* attribute indicating
process exit status (may be None).

*callback* is a function which gets called every time a process
terminates (a Process instance is passed as callback argument).

Function will return as soon as all processes terminate or when
*timeout* occurs.
Differently from Process.wait() it will not raise TimeoutExpired if
*timeout* occurs.

Typical use case is:

- send SIGTERM to a list of processes
- give them some time to terminate
- send SIGKILL to those ones which are still alive

**Example**:

  
  >>> def on_terminate(proc):
  ...     print("process {} terminated".format(proc))
  ...
  >>> for p in procs:
  ...    p.terminate()
  ...
  >>> gone, alive = wait_procs(procs, timeout=3, callback=on_terminate)
  >>> for p in alive:
  ...     p.kill()

<a id="psutil.cpu_count"></a>

#### cpu\_count

```python
def cpu_count(logical=True)
```

Return the number of logical CPUs in the system (same as
os.cpu_count()).

If *logical* is False return the number of physical cores only
(e.g. hyper thread CPUs are excluded).

Return None if undetermined.

The return value is cached after first call.
If desired cache can be cleared like this:

>>> psutil.cpu_count.cache_clear()

<a id="psutil.cpu_times"></a>

#### cpu\_times

```python
def cpu_times(percpu=False)
```

Return system-wide CPU times as a namedtuple.
Every CPU time represents the seconds the CPU has spent in the
given mode. The namedtuple's fields availability varies depending on the
platform:

 - user
 - system
 - idle
 - nice (UNIX)
 - iowait (Linux)
 - irq (Linux, FreeBSD)
 - softirq (Linux)
 - steal (Linux >= 2.6.11)
 - guest (Linux >= 2.6.24)
 - guest_nice (Linux >= 3.2.0)

When *percpu* is True return a list of namedtuples for each CPU.
First element of the list refers to first CPU, second element
to second CPU and so on.
The order of the list is consistent across calls.

<a id="psutil.cpu_percent"></a>

#### cpu\_percent

```python
def cpu_percent(interval=None, percpu=False)
```

Return a float representing the current system-wide CPU
utilization as a percentage.

When *interval* is > 0.0 compares system CPU times elapsed before
and after the interval (blocking).

When *interval* is 0.0 or None compares system CPU times elapsed
since last call or module import, returning immediately (non
blocking). That means the first time this is called it will
return a meaningless 0.0 value which you should ignore.
In this case is recommended for accuracy that this function be
called with at least 0.1 seconds between calls.

When *percpu* is True returns a list of floats representing the
utilization as a percentage for each CPU.
First element of the list refers to first CPU, second element
to second CPU and so on.
The order of the list is consistent across calls.

**Examples**:

  
  >>> # blocking, system-wide
  >>> psutil.cpu_percent(interval=1)
  2.0
  >>>
  >>> # blocking, per-cpu
  >>> psutil.cpu_percent(interval=1, percpu=True)
  [2.0, 1.0]
  >>>
  >>> # non-blocking (percentage since last call)
  >>> psutil.cpu_percent(interval=None)
  2.9
  >>>

<a id="psutil.cpu_times_percent"></a>

#### cpu\_times\_percent

```python
def cpu_times_percent(interval=None, percpu=False)
```

Same as cpu_percent() but provides utilization percentages
for each specific CPU time as is returned by cpu_times().
For instance, on Linux we'll get:

  >>> cpu_times_percent()
  cpupercent(user=4.8, nice=0.0, system=4.8, idle=90.5, iowait=0.0,
             irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
  >>>

*interval* and *percpu* arguments have the same meaning as in
cpu_percent().

<a id="psutil.cpu_stats"></a>

#### cpu\_stats

```python
def cpu_stats()
```

Return CPU statistics.

<a id="psutil.virtual_memory"></a>

#### virtual\_memory

```python
def virtual_memory()
```

Return statistics about system memory usage as a namedtuple
including the following fields, expressed in bytes:

 - total:
   total physical memory available.

 - available:
   the memory that can be given instantly to processes without the
   system going into swap.
   This is calculated by summing different memory values depending
   on the platform and it is supposed to be used to monitor actual
   memory usage in a cross platform fashion.

 - percent:
   the percentage usage calculated as (total - available) / total * 100

 - used:
    memory used, calculated differently depending on the platform and
    designed for informational purposes only:
    macOS: active + wired
    BSD: active + wired + cached
    Linux: total - free

 - free:
   memory not being used at all (zeroed) that is readily available;
   note that this doesn't reflect the actual memory available
   (use 'available' instead)

Platform-specific fields:

 - active (UNIX):
   memory currently in use or very recently used, and so it is in RAM.

 - inactive (UNIX):
   memory that is marked as not used.

 - buffers (BSD, Linux):
   cache for things like file system metadata.

 - cached (BSD, macOS):
   cache for various things.

 - wired (macOS, BSD):
   memory that is marked to always stay in RAM. It is never moved to disk.

 - shared (BSD):
   memory that may be simultaneously accessed by multiple processes.

The sum of 'used' and 'available' does not necessarily equal total.
On Windows 'available' and 'free' are the same.

<a id="psutil.swap_memory"></a>

#### swap\_memory

```python
def swap_memory()
```

Return system swap memory statistics as a namedtuple including
the following fields:

 - total:   total swap memory in bytes
 - used:    used swap memory in bytes
 - free:    free swap memory in bytes
 - percent: the percentage usage
 - sin:     no. of bytes the system has swapped in from disk (cumulative)
 - sout:    no. of bytes the system has swapped out from disk (cumulative)

'sin' and 'sout' on Windows are meaningless and always set to 0.

<a id="psutil.disk_usage"></a>

#### disk\_usage

```python
def disk_usage(path)
```

Return disk usage statistics about the given *path* as a
namedtuple including total, used and free space expressed in bytes
plus the percentage usage.

<a id="psutil.disk_partitions"></a>

#### disk\_partitions

```python
def disk_partitions(all=False)
```

Return mounted partitions as a list of
(device, mountpoint, fstype, opts) namedtuple.
'opts' field is a raw string separated by commas indicating mount
options which may vary depending on the platform.

If *all* parameter is False return physical devices only and ignore
all others.

<a id="psutil.disk_io_counters"></a>

#### disk\_io\_counters

```python
def disk_io_counters(perdisk=False, nowrap=True)
```

Return system disk I/O statistics as a namedtuple including
the following fields:

 - read_count:  number of reads
 - write_count: number of writes
 - read_bytes:  number of bytes read
 - write_bytes: number of bytes written
 - read_time:   time spent reading from disk (in ms)
 - write_time:  time spent writing to disk (in ms)

Platform specific:

 - busy_time: (Linux, FreeBSD) time spent doing actual I/Os (in ms)
 - read_merged_count (Linux): number of merged reads
 - write_merged_count (Linux): number of merged writes

If *perdisk* is True return the same information for every
physical disk installed on the system as a dictionary
with partition names as the keys and the namedtuple
described above as the values.

If *nowrap* is True it detects and adjust the numbers which overflow
and wrap (restart from 0) and add "old value" to "new value" so that
the returned numbers will always be increasing or remain the same,
but never decrease.
"disk_io_counters.cache_clear()" can be used to invalidate the
cache.

On recent Windows versions 'diskperf -y' command may need to be
executed first otherwise this function won't find any disk.

<a id="psutil.net_io_counters"></a>

#### net\_io\_counters

```python
def net_io_counters(pernic=False, nowrap=True)
```

Return network I/O statistics as a namedtuple including
the following fields:

 - bytes_sent:   number of bytes sent
 - bytes_recv:   number of bytes received
 - packets_sent: number of packets sent
 - packets_recv: number of packets received
 - errin:        total number of errors while receiving
 - errout:       total number of errors while sending
 - dropin:       total number of incoming packets which were dropped
 - dropout:      total number of outgoing packets which were dropped
                 (always 0 on macOS and BSD)

If *pernic* is True return the same information for every
network interface installed on the system as a dictionary
with network interface names as the keys and the namedtuple
described above as the values.

If *nowrap* is True it detects and adjust the numbers which overflow
and wrap (restart from 0) and add "old value" to "new value" so that
the returned numbers will always be increasing or remain the same,
but never decrease.
"net_io_counters.cache_clear()" can be used to invalidate the
cache.

<a id="psutil.net_connections"></a>

#### net\_connections

```python
def net_connections(kind='inet')
```

Return system-wide socket connections as a list of
(fd, family, type, laddr, raddr, status, pid) namedtuples.
In case of limited privileges 'fd' and 'pid' may be set to -1
and None respectively.
The *kind* parameter filters for connections that fit the
following criteria:

+------------+----------------------------------------------------+
| Kind Value | Connections using                                  |
+------------+----------------------------------------------------+
| inet       | IPv4 and IPv6                                      |
| inet4      | IPv4                                               |
| inet6      | IPv6                                               |
| tcp        | TCP                                                |
| tcp4       | TCP over IPv4                                      |
| tcp6       | TCP over IPv6                                      |
| udp        | UDP                                                |
| udp4       | UDP over IPv4                                      |
| udp6       | UDP over IPv6                                      |
| unix       | UNIX socket (both UDP and TCP protocols)           |
| all        | the sum of all the possible families and protocols |
+------------+----------------------------------------------------+

On macOS this function requires root privileges.

<a id="psutil.net_if_addrs"></a>

#### net\_if\_addrs

```python
def net_if_addrs()
```

Return the addresses associated to each NIC (network interface
card) installed on the system as a dictionary whose keys are the
NIC names and value is a list of namedtuples for each address
assigned to the NIC. Each namedtuple includes 5 fields:

- family: can be either socket.AF_INET, socket.AF_INET6 or
psutil.AF_LINK, which refers to a MAC address.
- address: is the primary address and it is always set.
- netmask: and 'broadcast' and 'ptp' may be None.
- ptp: stands for "point to point" and references the
destination address on a point to point interface
(typically a VPN).
- broadcast: and *ptp* are mutually exclusive.

Note: you can have more than one address of the same family
associated with each interface.

<a id="psutil.net_if_stats"></a>

#### net\_if\_stats

```python
def net_if_stats()
```

Return information about each NIC (network interface card)
installed on the system as a dictionary whose keys are the
NIC names and value is a namedtuple with the following fields:

 - isup: whether the interface is up (bool)
 - duplex: can be either NIC_DUPLEX_FULL, NIC_DUPLEX_HALF or
           NIC_DUPLEX_UNKNOWN
 - speed: the NIC speed expressed in mega bits (MB); if it can't
          be determined (e.g. 'localhost') it will be set to 0.
 - mtu: the maximum transmission unit expressed in bytes.

<a id="psutil.boot_time"></a>

#### boot\_time

```python
def boot_time()
```

Return the system boot time expressed in seconds since the epoch
(seconds since January 1, 1970, at midnight UTC). The returned
value is based on the system clock, which means it may be affected
by changes such as manual adjustments or time synchronization (e.g.
NTP).

<a id="psutil.users"></a>

#### users

```python
def users()
```

Return users currently connected on the system as a list of
namedtuples including the following fields.

 - user: the name of the user
 - terminal: the tty or pseudo-tty associated with the user, if any.
 - host: the host name associated with the entry, if any.
 - started: the creation time as a floating point number expressed in
   seconds since the epoch.

