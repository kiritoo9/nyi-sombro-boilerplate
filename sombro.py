import time
from rich.console import Console
from generator.model import ModelGenerator
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# Show prompt
greetings = """
Wilujeng sumping kang, mangga pilih naon anu anjeun generate:

1. Generate Model dari Database
2. Generate CRUD (nanti bisa milih tablenya)
"""

print("\n")
print(Panel(greetings, title="Nyi Sombro Cli - Generator", subtitle="author: @kiritoo9 - version 1.1", width=60))

# console.print(questions, style="purple")
try:
    choosen = int(Prompt.ask("\nSok asupkeun pilihan maneh :moai:"))
    if choosen > 2:
        console.print(f"\nHampura kang, teu aya pilihan nomer {choosen} :smiley:")
    else:
        with console.status("Punten kang diantosan sakedap", spinner="aesthetic"):
            time.sleep(1)
            if choosen == 1:
                ModelGenerator()
                console.print("\nAlhamdulillah kabéh tabel dina database anjeun geus dihasilkeun, nuhun kang :winking_face::folded_hands:", style="blue")
            elif choosen == 2:
                generate_crud()

except Exception as e:
    console.print(f"\nwkwkwk hampura kang masih aya error euy :laughing:\nieu kang error nya: [red]{str(e)}")