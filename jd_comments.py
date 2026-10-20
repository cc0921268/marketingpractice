import requests
import time
import re
import pandas as pd

# ========== 商品SKU，已经填好你刚才的京东商品 ==========
sku_id = "100013209930"
# ==========================================================

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": f"https://item.jd.com/{sku_id}.html"
    # 等下把Cookie粘贴到这里，格式示例： "Cookie":"shshshfpa=7d5e518d-7d65-ade4-ef87-c0f6c1c3f383-1765085900; shshshfpx=7d5e518d-7d65-ade4-ef87-c0f6c1c3f383-1765085900; __jdv=76161171|www.bing.com|-|referral|-|1792499040019; __jdu=1765085900277517970634; areaId=6; PCSYCityID=CN_140000_140700_0; is_avif=onAVIF; pinId=OpmoRqn0551wparO-P2I47V9-x-f3wj7; pin=jd_7248ef8a76596; unick=%E6%B6%94%E6%B6%94icatoi; ceshi3.com=000; _tp=8g%2Bmp6QeUm9rBq7kYd5RjRnWtsrn5lFzVoVgA4w1vVE%3D; _pst=jd_7248ef8a76596; o2State=; ipLoc-djd=6-336-44145-44339.7283315219; detailedAdd_coord=112.638699,37.672643; detailedAdd=%E5%B1%B1%E8%A5%BF%E6%99%8B%E4%B8%AD%E5%B8%82%E6%A6%86%E6%AC%A1%E5%8C%BA%E5%BC%A0%E5%BA%86%E4%B9%A1%E5%88%9B%E4%B8%9A%E8%A1%97839%E5%8F%B7%E5%B1%B1%E8%A5%BF%E6%99%8B%E4%B8%AD%E7%90%86%E5%B7%A5%E5%AD%A6%E9%99%A2%E8%8F%9C%E9%B8%9F%E9%A9%BF%E7%AB%99; detailedAdd_areaid=6-336-44145-44339; cn=1; wlfstk_smdl=z9rvswdywsta4cziftig9kjsn7n89cs9; 3AB9D23F7A4B3C9B=NBZ2XIW55GCJQC3AZMHIQA7HGWCD2CFUA4DNVASF3XCQ57JNWYGNIHOPPQOYZUUOTCP6KLFMNRXETCEVFHD2XME2FY; TrackID=1SQUPUKQyvIUH-C7FWi5GPlmKI8d7CmaVIbU19Ewz2jjc7axS4n3iDBWsZ5UvHc2Syvd7bUIG5_IK7Po5kWCkxhynip2aBm8rx1U1az2rpd5Hc6TEi_Ij0Q2HGbvQ1gvT; thor=A276A7B152AD133EC0D639FE2B8F25B50702EE68E4037E01F4946855C16BA2CFF6EBD1CC0331921DEB40EF637D9B6409B27962DD1F3F48F09740879E258D0DCF5565D77EB2D03882F787FC3CA0A020DA065EEC2EE255A8B78EA528FBD47770EA1604B3403F16FABBD9F6F9C06FACA371850B3C2BB58AD9DC9C257BFAE36A6B91CACA4496BDE828149E11B1D8A3C8FA700777AEF59F2B577CDEF0BCBF897618C1; light_key=AASBKE7rOxgWQziEhC_QY6yaonDODOSXpN32HHUxu-ai2TN-5UX3O7SLQTIpQvrS8mopE_5z; token=6f3f1cf2c0a7e42342a6275f0c341696,3,995833; 3AB9D23F7A4B3CSS=jdd03NBZ2XIW55GCJQC3AZMHIQA7HGWCD2CFUA4DNVASF3XCQ57JNWYGNIHOPPQOYZUUOTCP6KLFMNRXETCEVFHD2XME2FYAAAANBLFGZEUIAAAAACCQZXGT2TBSJIQX; mt_xid=V2_52007VwMUVVlZW14XSBhfA2EHElRVXlNdHUwpVQFmAkYBVV5ODUpMEEAANQsRTg1RWl8DGhhUUTcFQlNeUQAJL0oYXwJ7AxNOXllDWR5CG1kOZAUiUG1YYlwYQR9eAWQEGlRVaFdbFk8%3D; joyya=1792499667.0.28.0vtwevp; flash=3_P6AWdfWGR1raKfUabHZQorMIpt-jYbR4DVnYKOyKSfu1SMKIvuMgpCiHf5eAKb80EbNGZ3qttwDgHDaRrwNoglDqxJOoY3Qniza0wj9Xgjths8IGLuTZxK8h0T88UwuH51ZR20lB16LvXnaZR6vmxuGyZVqS9cipUlKJE41eetb8SSqrps_GLeYi; shshshfpb=BApXWgPtGWsRAqP-djyJDUF1OqYF6BUJZBidJXi9q9xJ1ItZfQtGExkLuinP7ZNAmKuP1xPSOsqFbcro07qRattMqMVuxqz4VwVoL; __jda=181111935.1765085900277517970634.1765085900.1787393402.1792499040.5; __jdb=181111935.20.1765085900277517970634|5.1792499040; __jdc=181111935; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17k-kb8WpsbIiaGx1aspULJ9T352wKr7cdXOFocwdnt8hy3qpfF12k0mCMpoMDMCOfXpQG3DTJbfHqrPPH77e3Qx7KQV6ZSSgCEkN-sT610wcQk94vH4XY9R3JK9rCFAJ3EpwCe3mSJAvqfEZSTL1Cqx1UwoAiJNHCQPgv1gRgdE-bcg",
}

url = "https://club.jd.com/comment/productPageComments.action"
all_comments = []

for page in range(0, 10):  # 爬前10页
    params = {
        "callback": "fetchJSON_comment98",
        "productId": sku_id,
        "score": 0,
        "sortType": 5,
        "page": page,
        "pageSize": 10,
        "isShadowSku": 0,
        "fold": 1
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        json_str = re.search(r'fetchJSON_comment98\((.*)\);', resp.text).group(1)
        data = pd.read_json(json_str)
        comments = data["comments"]
        for c in comments:
            all_comments.append({
                "id": c.get("id"),
                "star": c.get("score"),
                "review": c.get("content"),
                "time": c.get("creationTime")
            })
        print(f"✅ 第 {page+1} 页抓取成功")
        time.sleep(1.5)
    except Exception as e:
        print(f"❌ 第 {page+1} 页失败：{e}")
        break

df = pd.DataFrame(all_comments)
df.to_csv("jd_comments.csv", encoding="utf-8-sig", index=False)
print(f"\n总共抓取 {len(all_comments)} 条评论，已保存 jd_comments.csv")