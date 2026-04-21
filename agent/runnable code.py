import json
import re

# ---------------- LOAD ----------------
with open("reflection_tree.json", "r", encoding="utf-8") as f:
    nodes = json.load(f)

node_map = {n["id"]: n for n in nodes}

state = {
    "answers": {},
    "signals": {}
}

visit_count = {}

# ---------------- UTILS ----------------

def normalize(text):
    return str(text).strip().lower()

def replace_placeholders(text):
    if not text:
        return text

    def repl(match):
        key = match.group(1)

        # {A1_OPEN.answer}
        if ".answer" in key:
            node_id = key.split(".")[0]
            return state["answers"].get(node_id, "")

        # signals
        return state["signals"].get(key, "")

    return re.sub(r"\{([^}]+)\}", repl, text)


def get_children(node_id):
    return [n for n in nodes if str(n["parentId"]) == str(node_id)]


def safe_input(options):
    while True:
        try:
            choice = int(input("Choose: ")) - 1
            if 0 <= choice < len(options):
                return options[choice]
        except:
            pass
        print("Invalid input. Try again.")


# ---------------- ENGINE ----------------

def run():
    current = "START"

    while True:

        # Loop protection
        visit_count[current] = visit_count.get(current, 0) + 1
        if visit_count[current] > 10:
            raise Exception(f"Infinite loop detected at {current}")

        node = node_map[current]
        text = replace_placeholders(node.get("text", ""))

        if text:
            print("\n" + text)

        node_type = node["type"]

        # -------- START --------
        if node_type == "start":
            children = get_children(current)
            if not children:
                raise Exception("START has no child")
            current = children[0]["id"]

        # -------- QUESTION --------
        elif node_type == "question":
            options = node.get("options", "").split("|")

            for i, opt in enumerate(options):
                print(f"{i+1}. {opt}")

            answer = safe_input(options)

            # store answer
            state["answers"][node["id"]] = answer

            # 🔥 FIX: store actual answer as signal value
            signal = node.get("signal")
            if signal:
                state["signals"][signal] = answer

            children = get_children(current)
            if not children:
                raise Exception(f"No child for {node['id']}")

            current = children[0]["id"]

        # -------- DECISION --------
        elif node_type == "decision":
            rules_text = (node.get("target", "") or "") + ";" + (node.get("options", "") or "")
            rules = [r.strip() for r in rules_text.split(";") if r.strip()]

            parent_answer = state["answers"].get(node["parentId"], "")
            next_node = None

            for rule in rules:
                if not rule.startswith("answer="):
                    continue
                if ":" not in rule:
                    continue

                condition, target = rule.split(":", 1)
                expected = condition.replace("answer=", "").strip()

                if normalize(parent_answer) == normalize(expected):
                    next_node = target.strip()
                    break

            if not next_node:
                print("\n[DEBUG ERROR]")
                print("Node:", node["id"])
                print("Answer:", parent_answer)
                print("Rules:", rules)
                raise Exception("Decision mapping failed")

            current = next_node

        # -------- REFLECTION --------
        elif node_type == "reflection":
            signal = node.get("signal")

            # handle signals like axis2:tracking=enabled
            if signal:
                if "=" in signal:
                    key, value = signal.split("=", 1)
                    state["signals"][key.strip()] = value.strip()

            children = get_children(current)

            # 🔥 FIX: handle missing child (A3_R_WEAK case)
            if not children:
                if current.startswith("A3_R_WEAK"):
                    current = "SUMMARY"
                    continue

                print(f"[WARN] No child for {node['id']}, ending safely.")
                current = "END"
                continue

            current = children[0]["id"]

        # -------- BRIDGE --------
        elif node_type == "bridge":
            signal = node.get("signal")

            if signal:
                state["signals"][signal] = "complete"

            target = node.get("target")
            if not target:
                raise Exception(f"Bridge missing target at {node['id']}")

            current = target

        # -------- SUMMARY --------
        elif node_type == "summary":
            print("\n--- SUMMARY ---")
            print(text)

            current = "END"

        # -------- END --------
        elif node_type == "end":
            print("\nDone.")
            break

        else:
            raise Exception(f"Unknown node type: {node_type}")


# ---------------- RUN ----------------

if __name__ == "__main__":
    run()
