
import requests

text = ("涩谷站前十字路口每天有超过两百万行人穿过，"
          "被称为世界上最繁忙的十字路口。"
          "今年春天新开业的涩谷樱花塔高达四十七层，"
          "顶层观景台可以同时眺望富士山和东京晴空塔。"
          "地下三层直通涩谷站，连接了银座线、副都心线、东急东横线和埼京线。"
          "塔内入驻了两百家商铺，从古着店到米其林一星寿司应有尽有。"
          "二十一楼设立了二十四小时创业孵化器，免费提供高速网络和电源。"
          "涩谷区区长说希望这里成为年轻人梦想开始的地方。")

token = requests.post("http://127.0.0.1:8000/token", data={"username": "test", "password": "123"}).json()["access_token"]

r = requests.post("http://127.0.0.1:8000/articles", json={"title": "涩谷新地标", "content": text}, headers={"Authorization": f"Bearer {token}"})
aid = r.json()["id"]
print("创建:", r.status_code, aid)

s = requests.post(f"http://127.0.0.1:8000/articles/{aid}/summarize").json()
print("摘要:", s["summary"])
