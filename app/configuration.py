file = open("backgroundColor.txt", "r")
color = file.read()
file.close()


def update():
    file = open("backgroundColor.txt", "r")
    color = file.read()
    file.close()
    config["backgroundColor"] = color


config = {
    "backgroundColor": color
}
