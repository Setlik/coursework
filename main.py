from src.views import generate_json_response


def main():
    result_json = generate_json_response("2021-10-01 14:00:00")
    print(result_json)


if __name__ == "__main__":
    main()
