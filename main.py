from rich.console import Console
console = Console()
version = open('version.txt','r').read()
Logo = f"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
|     .-.
|    /   \         .-.
|   /     \       /   \       .-.     .-.     _   _         
+--/-------\-----/-----\-----/---\---/---\---/-\-/-\/\/---   | G-ToolKit
| /         \   /       \   /     '-'     '-'                | v.{version}
|/           '-'         '-'
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

console.print(Logo,style="bold green")