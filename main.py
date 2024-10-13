from src.views import generate_json_response


def main():
    result_json = generate_json_response()
    print(result_json)

if __name__ == "__main__":
    main()