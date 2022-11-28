import json

with open(f"./databases/users.json") as f:
    users = json.load(f)

while True:
    name = input("이름을 입력해주세요: ")
    if name=="q": break
    info = {"pw": "123", "type": "student", "timeTable": [], "attendance": 0, "importance": 0}
    info["group"] = "team" + input("팀 번호를 입력해주세요: ")
    info["leader"] = int(input("조장인가요?: "))
    users[name] = info

with open(f"./databases/users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=4, ensure_ascii=False)