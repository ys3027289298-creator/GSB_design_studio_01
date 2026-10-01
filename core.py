import json


def new_game():
    return {"items": {}, "load": 0, "capacity": 2, "stock": 100, "metric": 100, "day": 1, "id": 0, "fault": False, "resource": 10, "rate": 2, "clock": 0, "paused": False, "settled": False}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def _settled(state):
    return state.get("settled", False)


def add(state, item_id, amount):
    if _settled(state) or item_id in state["items"] or amount <= 0 or amount > state["stock"]:
        return False
    state["items"][item_id] = amount
    state["stock"] -= amount
    return True


def receive(state, item_id):
    if _settled(state) or state["load"] >= state["capacity"]:
        return False
    state["load"] += 1
    return True


def fee(state, item_id, end_day):
    return (end_day - state["day"]) * state["rate"]


def cancel(state, item_id):
    if _settled(state) or item_id not in state["items"]:
        return False
    state["stock"] += state["items"].pop(item_id)
    return True


def produce(state, amount):
    return not _settled(state) and not state["fault"] and amount > 0


def event(state):
    if _settled(state):
        return False
    state["metric"] -= 10
    return state["metric"]


def guard(state, item_id):
    amount = state["items"].get(item_id)
    return not _settled(state) and amount is not None and state["resource"] >= amount


def tick(state):
    if state.get("paused", False) or _settled(state):
        return state["clock"]
    state["clock"] += 1
    return state["clock"]


def settle(state):
    state["settled"] = True
    return True


def main():
    print("命令: add/receive/fee/cancel/produce/event/guard/tick/settle/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
