import requests, json, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd


class Awvs(object):
    def __init__(self):
        self.host = "https://127.0.0.1:13443/"
        api_key = "1986ad8c0a5b3df4d7028d5f3c06e936ca0857fbc89034d1d9d7cd29eb7755603"
        self.api_header = {'X-Auth': api_key, 'content-type': 'application/json'}
        self.awvs_scan_rule = {
            "full": "11111111-1111-1111-1111-111111111111",
            "highrisk": "11111111-1111-1111-1111-111111111112",
            "XSS": "11111111-1111-1111-1111-111111111116",
            "SQL": "11111111-1111-1111-1111-111111111113",
            "Weakpass": "11111111-1111-1111-1111-111111111115",
            "crawlonly": "11111111-1111-1111-1111-111111111117"
        }

    def del_http_head(self, domain):
        if "https://" in domain:
            domain1 = domain.replace("https://", "")
            return domain1
        elif "http://" in domain:
            domain1 = domain.replace("http://", "")
            return domain1

    def get_targets_id(self, domain):
        domain1 = self.del_http_head(domain)
        try:
            r = requests.get(self.host + "/api/v1/targets?q=%s" % (domain1), headers=self.api_header, timeout=10,
                             verify=False)
            result = json.loads(r.content)
            if (r.status_code == 200):
                return result
        except Exception as e:
            return str(e)

    def add_target(self, domain):
        data = {"address": domain, "description": domain, "criticality": "10"}
        try:
            response = requests.post(self.host + "/api/v1/targets", data=json.dumps(data), headers=self.api_header,
                                     timeout=30, verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except requests.exceptions.ConnectionError as e:
            return str(e)

    def start_scan(self, domainlist):
        success = []
        result = {}
        if len(domainlist) > 1:
            for domain in domainlist:
                target_id = self.add_target(domain)  # 添加域名，并返回target_id
                result['targetid'] = target_id
                result['domain'] = domain
                success.append(result)
                data = {
                    'target_id': target_id,
                    'profile_id': self.awvs_scan_rule['full'],
                    'schedule':
                        {'disable': False,
                         'start_date': None,
                         'time_sensitive': False
                         }
                }
                try:
                    r = requests.post(url=self.host + '/api/v1/scans', timeout=10, verify=False,
                                      headers=self.api_header, data=json.dumps(data))
                    result = json.loads(r.content)
                    success.append(result)

                except Exception as e:
                    return {"msg": "扫描程序异常,请联系安全部门"}
        count = len(success)
        return {"count": count, "success": success}

    def get_scan_id(self, domain):
        get_target = self.get_targets_id(domain)
        if len(get_target.get('targets')) > 0:
            targetid = get_target.get('targets')[0]['target_id']
        try:
            r = requests.get(url=self.host + '/api/v1/scans?q=target_id:{}'.format(targetid), timeout=10,
                             verify=False, headers=self.api_header)
            result = json.loads(r.content)
            scanid = result.get('scans')[0]['scan_id']
            status = result.get('scans')[0]['current_session']['status']
            return {"scan_status": status, "scan_id": scanid}
        except Exception as e:
            return False

    def get_scan_result(self, domain):
        scan = self.get_scan_id(domain)
        if scan:
            if scan['scan_status'] == "completed":
                scanid = scan['scan_id']
                try:
                    r = requests.get(url=self.host + '/api/v1/scans/{}/results'.format(scanid), timeout=10,
                                     verify=False, headers=self.api_header)
                    result = json.loads(r.content)
                    print(result)
                    resultid = result.get('results')[0]['result_id']
                    # print(resultid,status)
                    path = "/api/v1/scans/{}/results/{}/vulnerabilities".format(scanid, resultid)
                    print(path)
                    r1 = requests.get(
                        url=self.host + '/api/v1/scans/{}/results/{}/vulnerabilities'.format(scanid, resultid),
                        timeout=10, verify=False, headers=self.api_header)
                    result1 = json.loads(r1.content)
                    return result1
                except Exception as e:
                    return str(e)
            else:
                return {"status": 401, "msg": "扫描未完成，无法获取扫描结果"}
        else:
            return {"status": 500, "msg": "该域名未添加扫描"}

    # 生成报告需要5～10秒时间，仅支持获取单个扫描报告
    def report(self, domain):
        scan = self.get_scan_id(domain)
        if scan:
            if scan['scan_status'] == "completed":
                scan_id = scan['scan_id']
                data = {
                    "template_id": "11111111-1111-1111-1111-111111111112",
                    "source":
                        {
                            "description": domain,
                            "list_type": "scans",
                            "id_list": [scan_id]
                        }
                }
                try:
                    req = requests.get(url=self.host + "/api/v1/reports", timeout=10, verify=False,
                                       headers=self.api_header)
                    json_content = json.loads(req.content)
                    # print(scan_id)
                    # print(json_content)
                    if scan_id in req.text:  # 判断scan_id是否已经生成报告
                        result = json.loads(req.content)
                        reports = result.get('reports')
                        # print(reports)
                        df = pd.DataFrame(reports)
                        ld = df.drop('source', 1).assign(**pd.DataFrame(df.source.values.tolist()))
                        newdf = ld.id_list.apply(pd.Series)
                        index = newdf[(newdf[0] == scan_id)].index.item()
                        print(index)
                        reportdetail = reports[index]
                        return reportdetail

                    else:
                        # return "111"
                        r1 = requests.post(url=self.host + '/api/v1/reports', timeout=10, verify=False,
                                           headers=self.api_header, data=json.dumps(data))
                        report_url = r1.headers.get('Location')
                        time.sleep(8)
                        r2 = requests.get(url=self.host + report_url, timeout=10, verify=False,
                                          headers=self.api_header)
                        return json.loads(r2.content)

                except Exception as e:
                    return {"status": 111}

            else:
                return {"status": 401, "msg": "扫描未完成，无法获取报告"}
        else:
            return {"status": 500, "msg": "该域名未添加扫描"}

    # def get_report(self,domain):
    #     try:
    #         r = requests.get(url=define.host + '/api/v1/reports', timeout=10, verify=False, headers=define.api_header)
    #         content =  r.content
    #         if self.get_scan_id(domain)


if __name__ == "__main__":
    A = Awvs()
    test = A.start_scan("https://www.lol1234.com")
    print(test)
    # test = A.single_scan("https://joybear.com")
    # print(test)
    # print(Awvs.api_get('info'))
