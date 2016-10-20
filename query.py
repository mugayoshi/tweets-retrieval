def get_query(self, keywords,
          retweets=False,
          since="",
          until="",
          geocode="",):
    q = " OR ".join(keywords)
    q += ("" if retweets else " -filter:retweets")
    q += (" since:" + since if since else "")
    q += (" until:" + until if until else "")
    return q
