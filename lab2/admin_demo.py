import redis


def admin_menu():
    print(10 * "*", "Admin menu", 10 * "*")
    print("1. Users online")
    print("2. Top senders")
    print("3. Top spammers")
    print("4. Exit")
    return int(input("Please, choose action to take "))


def main():
    is_running = True
    connection = redis.Redis(charset="utf-8", decode_responses=True)

    while is_running:
        choice = admin_menu()

        if choice == 1:
            show_online_users(connection)

        elif choice == 2:
            show_top_senders(connection)

        elif choice == 3:
            show_top_spammers(connection)

        elif choice == 4:
            print("Exiting...")
            is_running = False
        else:
            print("Wrong option selection. Enter any key to try again..")


def show_top_spammers(connection):
    top_spammers_count = 10
    spammers = connection.zrange("spam:", 0, top_spammers_count, desc=True, withscores=True)
    print("Top %s spammers" % top_spammers_count)
    for index, spammer in enumerate(spammers):
        print(index + 1, ". ", spammer[0], " - ", int(spammer[1]), " spammed message(s)")


def show_top_senders(connection):
    top_senders_count = 10
    senders = connection.zrange("sent:", 0, top_senders_count, desc=True, withscores=True)
    print("Top %s senders" % top_senders_count)
    for index, sender in enumerate(senders):
        print(index + 1, ". ", sender[0], " - ", int(sender[1]), "message(s)")


def show_online_users(connection):
    online_users = connection.smembers("online:")
    print("Users online:")
    for user in online_users:
        print(user)


if __name__ == '__main__':
    main()
