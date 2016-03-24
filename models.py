


class Transfer:
    def __init__(self, ip_address, timestamp, request, response_code,
                 bytes_transfered, referrer, user_agent):
        self.ip_address = ip_address
        self.timestamp = timestamp.split()[0]
        self.request = request
        self.response_code = response_code
        self.bytes_transfered = bytes_transfered
        self.referrer = referrer
        self.user_agent = user_agent

    def __repr__(self):
        return "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(self.ip_address,
                                                   self.timestamp, self.request,
                                                   self.response_code,
                                                   self.bytes_transfered,
                                                   self.referrer,
                                                   self.user_agent)
