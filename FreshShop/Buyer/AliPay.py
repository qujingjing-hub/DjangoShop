from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0bIed2r/KZXSKMahA1srQPlij5Wz6Sm7ro2T2PgD/iBMIIvph6vN2WMBtBzBpUehvK6+MuzELL92FSASEL+ypTLdDhlneo0519BCgOGCmuTBTxDCWHecdn28/ddbNXeFFOPGhbTieW3KcQu3FeJgxCyqxi0RLdPnFLQzy9c+JQPiWUlJDXLKrdO5bi1BD0po3El5gluFK57VOIAh5RdR5WQXw0ikjNAbH55/zjYM7jnJWAzJVUaw5W/DSVYMN8SCTaJC8BnVxwbrhkkR/Jj5ZrkHybUMnZXddD6UJNqQMX7SE+oLzsmHNnh1th6xUcYG+7OdjslAsVQFI6m6skyQsQIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0bIed2r/KZXSKMahA1srQPlij5Wz6Sm7ro2T2PgD/iBMIIvph6vN2WMBtBzBpUehvK6+MuzELL92FSASEL+ypTLdDhlneo0519BCgOGCmuTBTxDCWHecdn28/ddbNXeFFOPGhbTieW3KcQu3FeJgxCyqxi0RLdPnFLQzy9c+JQPiWUlJDXLKrdO5bi1BD0po3El5gluFK57VOIAh5RdR5WQXw0ikjNAbH55/zjYM7jnJWAzJVUaw5W/DSVYMN8SCTaJC8BnVxwbrhkkR/Jj5ZrkHybUMnZXddD6UJNqQMX7SE+oLzsmHNnh1th6xUcYG+7OdjslAsVQFI6m6skyQsQIDAQABAoIBADZ4jnF22dFzmaP99NVqWVIHdhLWUGXA8X/mRwGVa3QX766EqaUUe+R8U3T2A1drxBe/TKjt2AfHtGTIb+jp4v4GuGVxM/Ahv2TQNHZGHiceRRjEwbc5WutsvisyRf8djPRgNrGEy0+/tVaoNGb65ygOck4IZu4AnYZDSTEqOHpkj13VKtdqyXlKhOhyrBCsIpvi4t/EnrXSoHSW4rPBG6Zl+rGJL29+eD+Ct7nX3iFCrbtsBYfPefg9KP38fCuFWPfBgyLerb+LrHac9Ku8WlgS+H1GdWRAUH6Lx8On2AaN7eXOEcRkYndWDhmy9jmVGA41ESBbxcOSb2V9ONz1oAECgYEA9C+P17YUO+j4HRay3qk28IWe4QxYGUovSs6VYFSq3FIfVL+3tnGq2oIG7Y2cmU/69rc9LypWSIeO48kFqUPWClx+y6UeZUfVx0yzLHUjzNQBp3zcgHLiQxpCZv3OUEtbusyyQUj53gQEd7fB6ydhanhO+oSuoPqx1KjEd1VVzHkCgYEA29de2JxWXSTMPUJuhut8kEcvbRzgzDRsUYX0/gkl+NSwDbpdbUDzknNSaOusVtlr1JTf8uReGF75ZVlBE28YvzQb1/LlDeB+b0IbBShnm+ewY+fPH7wt/2vYePNTDSf46zEkq3K2DdU2UQE70BUMxGdJN+PlHkeXzILi4cQ0Z/kCgYB3WFOma2CCU4AIv5JWzz+B2NzpQ14/pgltN4C8n0UO/7g+dKF2syF9QHXgXwk9yWBweuiVh8y6ED8fR53Tt8sCL2jtYVt0xuJOUUd1IB+KOchBMv6WbQ/3GfuAWOYgSmSf7PHmhKNTBoWkeZR2uT2ciwaW3Ih5N2348S9s37FaiQKBgQCq4ggpm6xODpJrc73yRg23IH4u9GmQkZc470V2Saoodzq6EQkaKYirZ9TBFaAKikqVHXvOk9DIZNq6+tvovUyhI2IZRAbj+IKO/PV/1t5ig3/KyJ9pbZ7bkfrcWVdPPKjyOGrmke4NZpQn9yuFHTelWxvAw/aOyNun7n1pPFf4EQKBgFic3x8hJ0VPJtQkKsNAODdT7DNBhx4OQ65A3+V3imMV1SUUNmq12jmFdS2lv2n33k4feEg7+xJa5263oedYXZ5GaiLhTwEyv/nWPuMPkFuibaxppgj8/MkX9AjNsum0s7dxmWNHFQPVS71gOsTCWSKrnhP9CJCwBKyZM9EEaQzL
-----END RSA PRIVATE KEY-----"""



# 实例化支付应用
alipay = AliPay(
    appid="2016101000652490",
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2"
)

#发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="334556", #订单号
    total_amount=str(100000.00), #支付金额
    subject="生鲜交易", #交易主题
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_string)