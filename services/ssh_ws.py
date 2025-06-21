import subprocess

def create_ssh_account(user_id):
    try:
        result = subprocess.run(["bash", "scripts/create_ssh_ws.sh", str(user_id)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Gagal membuat akun:\n{result.stderr}"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
