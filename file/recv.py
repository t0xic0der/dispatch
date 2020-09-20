from flask import Flask, request
import requests, hashlib, os, logging

main = Flask(__name__)
loge = logging.getLogger("werkzeug")
loge.disabled = True

@main.route("/recvarch/", methods=["POST"])
def recvarch():
    if request.method == "POST":
        f = request.files["files"]
        print(" * Transfer buffer cached to storage")
        f.save(f.filename+".bak")
        return {"respcode": "donesend"}


@main.route("/connsend/", methods=["GET"])
def connsend():
    if request.method == "GET":
        print(" * Identity proven to a sender")
        return {"hash": hashlib.sha512(request.get_json()["password"].encode("utf8")).hexdigest()}


@main.route("/filechek/", methods=["GET"])
def filechek():
    try:
        if request.method == "GET":
            if hashlib.sha512(open(request.get_json()["name"], "rb").read()).hexdigest() == request.get_json()["hash"]:
                os.system("mv " + request.get_json()["name"] + " " + request.get_json()["name"][:-4])
                print(" * Cache integrity verified"+ "\n" + " * Transfer complete")
                return {"respcode": "verified"}
            os.system("rm " + request.get_json()["name"])
            return {"respcode": "verifail"}
    except Exception as expt:
        return {"respcode": str(expt)}


if __name__ == "__main__":
    print(" * IPv6 address is", requests.get("https://ipv6.icanhazip.com/").text, end="")
    main.run(port=9696, host="::")