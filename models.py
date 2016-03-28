class Transfer:
    def __init__(self, ip_address, timestamp, client_request, response,
                 bytes_transfered, referrer, user_agent):
        self.ip_address = ip_address
        self.timestamp = timestamp.split()[0]
        self.client_request = client_request.split()
        self.request_type = self.client_request[0]

        if len(self.client_request) > 1:
            self.request_resource = self.client_request[1]

        if len(self.client_request) > 2:
            self.request_protocol = self.client_request[2]

        self.server_response_code = response
        self.bytes_transfered = bytes_transfered
        self.referrer = referrer
        self.user_agent = user_agent

    def __repr__(self):
        return"""
IP: {}
Timestamp: {}
Request: {}
Resource: {}
Server Response: {}
Bytes Transfered: {}
Referer: {}
User Agent: {}
""".format(self.ip_address, self.timestamp, self.request_type,
           self.request_resource, self.server_response_code,
           self.bytes_transfered, self.referrer, self.user_agent)


class CustomerTracker:


    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.resources = []
        self.total_bytes = 0
        self.login_instances = []
        self.user_agents = set()

    def add_log(self, log):
        if log.ip_address != self.ip_address:
            print("Huston, we have a fuck-up")
        else:
            if hasattr(log, 'request_resource'):
                self.resources.append((log.timestamp, log.request_resource))
                if "customer/account/loginPost" in log.request_resource:
                    self.login_instances.append(log.request_resource)

            if log.bytes_transfered:
                self.total_bytes += int(log.bytes_transfered)

            self.user_agents.add(log.user_agent)

    def get_login_instances(self):
        package = (len(self.login_instances), self.login_instances)
        return package

    def __repr__(self):
        unique_resources = len(set(self.resources))
        res_num = len(self.resources)
        resource_diff = res_num - unique_resources

        msg = """
IP: {}
Total Bytes: {} bytes
Total Log-ins: {}
Total Resources: {}
Duplicate Resources: {}
User Agents Used: {}
""".format(self.ip_address, self.total_bytes, len(self.login_instances),
           res_num, resource_diff, len(self.user_agents))

        return msg
