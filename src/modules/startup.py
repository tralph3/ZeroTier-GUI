import subprocess
import os


class Startup():
    def get_zt_cli_exit_code(self) -> int:
        try:
            subprocess.check_output(["zerotier-cli"])
        except subprocess.CalledProcessError as e:
            return e.code
        return 0

    def copy_access_token(self) -> None:
        username = os.getlogin()
        os.system(
            f"pkexec bash -c "
            '"cp /var/lib/zerotier-one/authtoken.secret '
            f"/home/{username}/.zeroTierOneAuthToken && "
            f"chown {username}:{username} "
            f"/home/{username}/.zeroTierOneAuthToken && "
            "chmod 0600 "
            f'/home/{username}/.zeroTierOneAuthToken"'
        )
