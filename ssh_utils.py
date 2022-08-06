import warnings

warnings.simplefilter("ignore", Warning)
import pexpect


def connect_pem(ip: str, port: int, pem_path: str, user: str):
    s = pexpect.spawnu(f"ssh {user}@{ip} -p {port} -i {pem_path}")
    s.interact()


def connect_password(ip: str, port: int, user: str, password: str):
    s = pexpect.spawnu(f"ssh {user}@{ip} -p {port}")
    s.expect("assword:")
    s.send(password + "\r")
    s.interact()


def chmod600_pem(pem_path: str):
    s = pexpect.spawnu(f"chmod 600 {pem_path}")
    s.close()
