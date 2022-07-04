
FROM centos7

USER root

ARG ANSIBLE_VER=2.9.10
LABEL ansible-version=${ANSIBLE_VER}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo && \
    dnf config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo && \
    yum update -y && \
    yum install -y \
        docker-ce-cli

RUN pip3 --no-cache-dir install --upgrade pip

RUN /usr/sbin/setcap cap_ipc_lock=+ep /bin/vault
RUN pip3 --no-cache-dir install --upgrade \
        ansible==${ANSIBLE_VER} \
        boto3 \
        boto \
        dnspython \
        docker \
        molecule \
        passlib \
        hvac \
        ansible-modules-hashivault \
        ansible --version && \
        docker --version && \
        molecule --version && \
    ln -s /usr/bin/vault /usr/local/bin/vault && \
    pip3 show \
        boto3 \
        dnspython && \
    ansible-galaxy collection install community.kubernetes && \
    cp -pr  /root/.ansible/collections /usr/local/lib/python3.6/site-packages/ansible && \
    yum clean all && \
    rm -rf /var/cache/yum

USER dockeruser

WORKDIR /opt/app

ENTRYPOINT [ "ansible" ]

CMD ["--version"]
