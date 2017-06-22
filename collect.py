import sys
from typing import List
from common import get_twitter

def msg(s):
    sys.stderr.write(s + "\n")

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

def collect_urls(tweets, favCounts):
    """{ツイートID-連番: {ツイートID, ユーザID, 画像URL}の辞書を作成"""
    msg("collect " + str(len(tweets)) + " tweets.")
    dic = {}
    max_id = 0
    for tw in tweets:
        favs = tw["favorite_count"]
        tweet_id = tw["id"]
        screen_name = tw["user"]["screen_name"]
        max_id = tweet_id
        if favs < favCounts:
            continue
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
        msg("getting favs...")
        max_id = 0
        lst = []
        # 限界まで検索する
        for iii in range(30):
            msg(str(iii))
            if max_id == 0:
                lst = t.favorites.list(count=200)
                max_id, data = collect_urls(lst, 10)
            else:
                lst = t.favorites.list(count=200, max_id=max_id)
                max_id, data = collect_urls(lst, 10)
            dic.update(data)
            if len(lst) < 100:
                break
    # 指定されたリストからの取得
    #   対象リストの絞り込み -> リスト内のユーザーの一覧 -> ユーザIDからの画像取得
    mast_list = get_list_dict(t.lists.list(count=200))
    users = {}
    for lst in lists:
        msg("getting users from list: " + lst)
        list_id = mast_list[lst]
        for u in t.lists.members(list_id=list_id)["users"]:
            user_id = u["id_str"]
            screen_name = u["screen_name"]
            users[user_id] = screen_name
    for u in users.items():
        msg("getting tweet from user: " + u[1])
        max_id = 0
        # 限界まで検索する
        for iii in range(30):
            msg(str(iii))
            lst = []
            if max_id == 0:
                lst = t.statuses.user_timeline(user_id=u[0], count=200)
                max_id, data = collect_urls(lst, 100)
            else:
                lst = t.statuses.user_timeline(user_id=u[0], count=200, max_id=max_id)
                max_id, data = collect_urls(lst, 100)
            dic.update(data)
            if len(lst) < 100:
                break
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