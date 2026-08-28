from rich.console import Console

console = Console()

version = open("version.txt", "r").read().strip()

Logo = f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
|     .-.
|    /   \\         .-.
|   /     \\       /   \\       .-.     .-.     _   _
+--/-------\\-----/-----\\-----/---\\---/---\\---/-\\-/-\\/\\/---   | G-ToolKit
| /         \\   /       \\   /     '-'     '-'                | v.{version}
|/           '-'         '-'
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

console.print(Logo, style="bold green")


console.print("[bold green]01.[/] [bold white]OSINT[/]")
console.print("[bold green]02.[/] [bold white]Recon[/]")
console.print("[bold green]03.[/] [bold white]Scanning[/]")
console.print("[bold green]04.[/] [bold white]Web Security[/]")
console.print("[bold green]05.[/] [bold white]Network Security[/]")
console.print("[bold green]06.[/] [bold white]Authentication[/]")
console.print("[bold green]07.[/] [bold white]Vulnerability Analysis[/]")
console.print("[bold green]08.[/] [bold white]Exploitation[/]")
console.print("[bold green]09.[/] [bold white]Wireless Security[/]")
console.print("[bold green]10.[/] [bold white]Cloud Security[/]")
console.print("[bold green]11.[/] [bold white]Reverse Engineering[/]")
console.print("[bold green]12.[/] [bold white]Malware Analysis[/]")
console.print("[bold green]13.[/] [bold white]Digital Forensics[/]")
console.print("[bold green]14.[/] [bold white]Social Engineering[/]")
console.print("[bold green]15.[/] [bold white]Reporting[/]")
console.print("[bold green]16.[/] [bold white]Automation[/]")
console.print("[bold green]17.[/] [bold white]Utilities[/]")

menu_input = console.input(
        "[bold green][#] Choose An Option:[/] "
)

console.print(f"\n[bold green][+] Selected:[/] {menu_input}")
