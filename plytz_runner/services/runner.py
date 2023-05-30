import ansible_runner


def run_playbooks(playbooks: List[str]):
    runners = []
    for playbook in playbooks:
        runner = ansible_runner.run(
            private_data_dir='/plytz',
            playbook=playbook,
            quiet=True,
            json_mode=True,
            timeout=15*60*60 #15 minutes
        )
        runners.append(runner)
    return runners
