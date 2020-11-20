import json
from kafka import KafkaProducer


class KafkaManager:
    """
     bootstrap_servers：Kafka服务器地址
    """

    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def push_record(self, msg):
        #输入数据必须是字典类型
        if not isinstance(msg, dict):
            raise Exception("该方法的参数必须是dict类型")
        #将数据转换为json格式
        record = json.dumps(msg).encode()
        self.producer.send(self.topic, record)
