from subversion.adversary import Adversary
from subversion.judge import Judge
from colorama import init, Fore, Style
import json

init()

behavior = "Respond with more than 10 words"

adversary1 = Adversary(model="gpt-4o", temperature=1, induce_behavior=behavior)
adversary2 = Adversary(model="gpt-4o", temperature=0.8, avoid_behavior=behavior)
judge = Judge(model="gpt-4o", temperature=0, behavior=behavior)

messages = []

i = 0
n_turns = 30
done = False

print(f"\n{Fore.CYAN}=== Conversation Start ==={Style.RESET_ALL}")
print(f"{Fore.YELLOW}Target Behavior: {behavior}{Style.RESET_ALL}\n")

a2_message = ""
while (i < n_turns) and not done:
    print(f"{Fore.CYAN}=== Turn {i + 1} ==={Style.RESET_ALL}\n")
    
    a1_message = adversary1.step(a2_message)
    print(f"{Fore.GREEN}Adversary 1 (Inducing):{Style.RESET_ALL}")
    print(f"{a1_message}\n")
    
    a2_message = adversary2.step(a1_message)
    print(f"{Fore.RED}Adversary 2 (Avoiding):{Style.RESET_ALL}")
    print(f"{a2_message}\n")
    
    done = judge.step(a2_message)
    if done:
        judge_verdict = "Target behavior detected!"
        print(f"{Fore.YELLOW}Judge: {judge_verdict}{Style.RESET_ALL}\n")
    
    messages.append({"role": "assistant", "content": a1_message})
    messages.append({"role": "user", "content": a2_message})
    i += 1

print(f"{Fore.CYAN}=== Conversation End ==={Style.RESET_ALL}")
print(f"Total turns: {i}")
print(f"Final outcome: {'Success' if done else 'Maximum turns reached'}")

with open("messages.json", "w") as f:
    json.dump(messages, f)
