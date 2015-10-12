
def increase_visits_count(sid, tx):
    short_url = tx.short_urls.get(sid)
    if short_url:
        short_url.increase_visits()
        tx.commit()