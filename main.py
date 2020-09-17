def loadconfig():
    with open('busboard.config') as configfile:
        configs = []
        for line in configfile:
            configs.append(line[:-1])
        API-KEY = configs[0].split("=")[1]


def main():
    loadconfig()
    print("Welcome to BusBoard.")


if __name__ == "__main__": main()
