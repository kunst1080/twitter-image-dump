import sys
from typing import List
from common import get_twitter

def get_media_urls(tw):
    """ツイートに紐づく画像URLの一覧を取得"""
    arr = []
    if "extended_entities" in tw:
        entities = tw["extended_entities"]
        if "media" in entities:
            medias = entities["media"]
            for media in medias:
                media_url = media["media_url"]
                arr.append(media_url)
    return arr

def collect_urls(tweets):
    """{ツイートID-連番: {ツイートID, ユーザID, 画像URL}の辞書を作成"""
    dic = {}
    max_id = 0
    for tw in tweets:
        tweet_id = tw["id"]
        screen_name = tw["user"]["screen_name"]
        max_id = tweet_id
        for idx, url in enumerate(get_media_urls(tw)):
            key = str(tweet_id) + "-" + str(idx)
            dic[key] = {"tweet_id": tweet_id, "screen_name": screen_name, "url": url}
    return [max_id, dic]

def get_list_dict(lists):
    """list_uriとlist_idの辞書を作成"""
    dic = {}
    for lst in lists:
        uri = lst["uri"]
        list_id = lst["id"]
        dic[uri] = list_id
    return dic

def main(use_fav: bool, lists: List):
    """
    use_fav … ふぁぼを対象にする場合true
    lists … 対象のリスト
    """
    t = get_twitter()
    dic = {}
    # ふぁぼ一覧の取得
    if use_fav:
        max_id = 0
        # 限界まで検索する
        for iii in range(30):
            if max_id == 0:
                max_id, data = collect_urls(t.favorites.list(count=200))
            else:
                max_id, data = collect_urls(t.favorites.list(count=200, max_id=max_id))
            if len(data) == 0:
                break
            dic.update(data)
    # 指定されたリストからの取得
    #   対象リストの絞り込み -> リスト内のユーザーの一覧 -> ユーザIDからの画像取得
    mast_list = get_list_dict(t.lists.list(count=200))
    users = {}
    for lst in lists:
        list_id = mast_list[lst]
        for u in t.lists.members(list_id=list_id)["users"]:
            user_id = u["id_str"]
            users[user_id] = user_id
    for u in users.keys():
        max_id = 0
        # 限界まで検索する
        for iii in range(30):
            if max_id == 0:
                max_id, data = collect_urls(t.statuses.user_timeline(user_id=u, count=200))
            else:
                max_id, data = collect_urls(
                    t.statuses.user_timeline(user_id=u, count=200, max_id=max_id))
            if len(data) == 0:
                break
            dic.update(data)
    # 標準出力へ
    for item in dic.values():
        tweet_id = item["tweet_id"]
        screen_name = item["screen_name"]
        url = item["url"]
        print(tweet_id, screen_name, url)

if __name__ == '__main__':
    """
    コマンドライン引数
    1 … 自分のふぁぼを対象にするかどうか(true/false)
    2以降 … DL対象のリストURI(例: 自分のID/lists/1)
    """
    use_fav = sys.argv[1] == "true"
    uri_list = []
    for i in range(2, len(sys.argv)):
        a = sys.argv[i]
        uri_list.append(a)
    main(use_fav, uri_list)