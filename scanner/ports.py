import asyncio


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
}

# Ports where the server waits for the client to speak first, so we send a
# minimal request to encourage a banner in response.
_CLIENT_FIRST_PORTS = {80: b"HEAD / HTTP/1.0\r\n\r\n", 8080: b"HEAD / HTTP/1.0\r\n\r\n"}


async def _grab_banner(reader, timeout):
    try:
        data = await asyncio.wait_for(reader.read(256), timeout=timeout)
        return data.decode(errors="ignore").strip().replace("\r", " ").replace("\n", " ")
    except (asyncio.TimeoutError, OSError):
        return ""


async def _probe_port(host, port, timeout):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(str(host), port), timeout=timeout
        )
    except (asyncio.TimeoutError, OSError):
        return None

    try:
        if port in _CLIENT_FIRST_PORTS:
            try:
                writer.write(_CLIENT_FIRST_PORTS[port])
                await writer.drain()
            except OSError:
                pass

        banner = await _grab_banner(reader, timeout)
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    return {
        "port": port,
        "service": COMMON_PORTS.get(port, "Unknown"),
        "banner": banner,
    }


async def _scan_ports_async(host, ports, timeout, max_concurrency):
    semaphore = asyncio.Semaphore(max_concurrency)

    async def bound_probe(port):
        async with semaphore:
            return await _probe_port(host, port, timeout)

    tasks = [asyncio.ensure_future(bound_probe(port)) for port in ports]
    results = await asyncio.gather(*tasks)

    open_ports = [r for r in results if r is not None]
    open_ports.sort(key=lambda r: r["port"])
    return open_ports


def scan_ports(host, ports=None, timeout=0.5, max_concurrency=50):
    """
    Scan a host's ports concurrently and grab a banner where available.

    Returns a list of dicts, one per open port:
        [{"port": 22, "service": "SSH", "banner": "SSH-2.0-OpenSSH_9.6"}, ...]
    """
    ports = list(ports) if ports is not None else list(COMMON_PORTS.keys())
    return asyncio.run(
        _scan_ports_async(host, ports, timeout=timeout, max_concurrency=max_concurrency)
    )