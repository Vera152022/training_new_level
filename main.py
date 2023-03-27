from flask import Flask, request, render_template, redirect
import random

signup_is_on = True

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/media/from_users'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def choice():
    if request.method == "GET":
        return render_template("major.html")
    elif request.method == "POST":
        if request.form["choice"] == "one":
            return redirect("/lesson/1")
        if request.form["choice"] == "two":
            return redirect("/lesson/2")
        if request.form["choice"] == "three":
            return redirect("/lesson/3")
        if request.form["choice"] == "four":
            return redirect("/lesson/4")
        if request.form["choice"] == "five":
            return redirect("/lesson/5")
        if request.form["choice"] == "six":
            return redirect("/lesson/6")
        print(request.form["choice"])


flag = 1
tot = []
good = 0


@app.route("/lesson/<int:site_id>", methods=["GET", "POST"])
def index1(site_id):
    global flag, tot, good
    if site_id == 1 and flag == 1:
        tot = plus_minus()
        flag = 0
    if site_id == 2 and flag == 1:
        tot = multiplication_division()
        flag = 0
    if site_id == 3 and flag == 1:
        tot = plus_minus_multiplication()
        flag = 0
    if site_id == 4 and flag == 1:
        tot = plus_minus_division()
        flag = 0
    if site_id == 5 and flag == 1:
        tot = multiplication_division_2()
        flag = 0
    if site_id == 6 and flag == 1:
        tot = multiplication()
        flag = 0
    if request.method == "GET":
        return render_template("lesson.html", ans=tot[0], total=tot[1])
    elif request.method == "POST":
        cells = list(request.form.keys())
        for i in range(20):
            if str(request.form[cells[i]]) == str(tot[1][i]):
                good += 1
        print(good)
        flag = 1
        return redirect(f"/result")


@app.route("/result", methods=["GET"])
def result():
    names = ['support_1', 'support_2', 'support_3', 'support_4', 'support_5']
    number = random.randint(0, 4)
    return render_template("result.html", name=names[number])


def plus_minus():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 100)
        number_2 = random.randint(1, 100)
        if i % 2 == 0:
            dictionary[i] = number + number_2
            example.append(f'{number} + {number_2} = ')
        if i % 2 == 1:
            if number <= number_2:
                dictionary[i] = number_2 - number
                example.append(f'{number_2} - {number} = ')
            else:
                dictionary[i] = number - number_2
                example.append(f'{number} - {number_2} = ')
    print(example)
    print(dictionary)
    return [example, dictionary]


def multiplication_division():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        if i % 2 == 0:
            number_2 = random.randint(1, 10)
            dictionary[i] = number * number_2
            example.append(f'{number} * {number_2} = ')
        if i % 2 == 1:
            number_2 = random.randint(1, 100)
            if number_2 % number == 0 and number <= number_2:
                dictionary[i] = number_2 // number
                example.append(f'{number_2} ÷ {number} = ')
            else:
                number_2 = number_2 + (number - (number_2 % number))
                dictionary[i] = number_2 // number
                example.append(f'{number_2} ÷ {number} = ')
    print(example)
    print(dictionary)
    return [example, dictionary]


def plus_minus_multiplication():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 0:
            dictionary[i] = number_2 * number_3 + number
            example.append(f'{number} + {number_2} * {number_3} = ')
        if i % 2 == 1:
            dictionary[i] = number_2 * number_3 - number
            example.append(f'{number_2} * {number_3} - {number} = ')
    return [example, dictionary]


def plus_minus_division():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 1:
            if number % number_2 == 0:
                dictionary[i] = number // number_2 + number_3
                example.append(f'{number_3} + {number} ÷ {number_2} = ')
            else:
                number = number + (number_2 - (number % number_2))
                dictionary[i] = number // number_2 + number_3
                example.append(f'{number_3} + {number} ÷ {number_2} = ')
        else:
            if number % number_2 == 0:
                if number % number_2 > number_3:
                    dictionary[i] = number // number_2 - number_3
                    example.append(f'{number} ÷ {number_2} - {number_3} = ')
                else:
                    dictionary[i] = number_3 - number // number_2
                    example.append(f'{number_3} - {number} ÷ {number_2} = ')
            else:
                number = number + (number_2 - (number % number_2))
                if number % number_2 > number_3:
                    dictionary[i] = number // number_2 - number_3
                    example.append(f'{number} ÷ {number_2} - {number_3} = ')
                else:
                    dictionary[i] = number_3 - number // number_2
                    example.append(f'{number_3} - {number} ÷ {number_2} = ')
    return [example, dictionary]


def multiplication_division_2():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 0:
            dictionary[i] = number_2 * number_3 * number
            example.append(f'{number} * {number_2} * {number_3} = ')
        if i % 2 == 1:
            if number * number_2 % number_3 == 0:
                dictionary[i] = number * number_2 // number_3
                example.append(f'{number} * {number_2} ÷ {number_3} = ')
            else:
                number_3 = 2
                while number_3 <= number * number_2:
                    if number * number_2 % number_3 == 0:
                        break
                    else:
                        number_3 += 1
                dictionary[i] = number * number_2 // number_3
                example.append(f'{number} * {number_2} ÷ {number_3} = ')
    return [example, dictionary]


def multiplication():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(2, 10)
        number_2 = random.randint(2, 10)
        dictionary[i] = number_2 * number
        example.append(f'{number} * {number_2} = ')
    return [example, dictionary]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
