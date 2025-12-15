from database import conversations_collection, sessions_collection


def main() -> None:
    orphans = []
    for session in sessions_collection.find({}, {"session_id": 1, "_id": 0}):
        sid = session.get("session_id")
        if not sid:
            continue
        if conversations_collection.count_documents({"session_id": sid}, limit=1) == 0:
            orphans.append(sid)

    if not orphans:
        print("No orphan sessions found.")
        return

    result = sessions_collection.delete_many({"session_id": {"$in": orphans}})
    print(f"Deleted {result.deleted_count} orphan sessions: {orphans}")


if __name__ == "__main__":
    main()
