#!/bin/bash

set -e

# 기본 경로 설정
BASEDIR=$(dirname $0)
BINDIR=$BASEDIR/bin

# Bash 환경 설정 로드
# source ~/.bashrc
source ~/.bash_profile

# 새로운 Conda 환경 생성 및 활성화
conda create -n dps python=3.8 -y  # Python 3.8을 사용하는 dps라는 환경 생성
conda activate dps

# 패키지 설치 및 설정
pip uninstall -y dps
python $BASEDIR/setup.py install

# 기존 Conda 환경 패키지가 있다면 삭제
if [ -f "$BINDIR/pyspark_conda_env.tar.gz" ]; then
  rm $BINDIR/pyspark_conda_env.tar.gz
fi

# Conda 환경 패키징 및 저장
if [[ "$SKIP_CONDA_PACK" != "1" ]]; then
  conda pack -n dps -o $BINDIR/.pyspark_conda_env.tar.gz  # 환경 이름을 지정하여 패킹
  mv $BINDIR/.pyspark_conda_env.tar.gz $BINDIR/pyspark_conda_env.tar.gz
fi

# 환경 비활성화 및 파일 권한 설정
conda deactivate
chmod 755 $BINDIR/pyspark_conda_env.tar.gz