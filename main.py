from src.views import generate_json_response


def main():
    date_input = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
    result_json = generate_json_response(date_input)
    print(result_json)

if __name__ == "__main__":
    main()