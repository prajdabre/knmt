model_config=$1
model_path=$2
input_file=$3
output_file="$input_file".trans
reference_file=$4
ppp_path=$5
tgt_lang=$6
decoding_method=$7

export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=

source /home/raj/softwares-and-scripts/virtualenv-15.1.0/basils/bin/activate

python /home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/eval.py $model_config $model_path $input_file $output_file --mode $decoding_method --beam_width 12 --nb_steps_ratio 1.5 --ref $reference_file --tgt_fn $reference_file --apply_preprocessing --apply_postprocessing --prepostprocessor $ppp_path --tgt_lang $tgt_lang --retrieve_activations --mb_size 1