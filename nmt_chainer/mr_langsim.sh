l1file=$1
l2file=$2
l1=$3
l2=$4
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=
export INDIC_RESOURCES_PATH=/home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/indic_nlp_library/indic_nlp_resources

source /home/raj/softwares-and-scripts/virtualenv-15.1.0/basils/bin/activate

python /home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/indic_nlp_library/src/utilities.py linguistic_similarity $l1file $l2file $l1 $l2