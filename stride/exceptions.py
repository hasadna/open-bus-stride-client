class StrideRequestFailedException(Exception):

    def __init__(self, status_code, text, msg=None):
        self.status_code = status_code
        self.text = text
        super(StrideRequestFailedException, self).__init__(
            "Failure response from Stride API ({}): {}".format(status_code, text) if not msg else msg
        )


class StrideRequestParsingException(StrideRequestFailedException):

    def __init__(self, status_code, text):
        super(StrideRequestParsingException, self).__init__(
            status_code, text,
            msg="Failed to parse response from Stride API ({}): {}".format(status_code, text)
        )
