save_path=$1
model_config=$2
model_path=$3
input_file=$4
reference_file=$5
ppp_path=$6
tgt_lang=$7
beam_width=$8
split_size=$9

rm -rf $save_path
mkdir -p $save_path
#split -a 3 -d -l 60 /windroot/raj/corpora_downloads/IWSLT2016/1s1t_ar_en/mlnmt.dev.tgt.raw $save_path/tgt-shard-
#split -a 3 -d -l 60 /windroot/raj/corpora_downloads/IWSLT2016/1s1t_ar_en/mlnmt.dev.src.raw $save_path/src-shard-

split -a 5 -d -l $split_size $input_file $save_path/src-shard-
split -a 5 -d -l $split_size $reference_file $save_path/tgt-shard-

num_shards=`ls $save_path/src-shard-* | wc -l `
echo "Number of shards to be processed:" $num_shards

for i in `seq -w 0 99999 | head -$num_shards`
do
	echo "nice -n 19 bash /home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/mr_decode.sh $model_config $model_path $save_path/src-shard-$i $save_path/tgt-shard-$i $ppp_path $tgt_lang $beam_width"
done > $save_path/gxp_instructions

source /home/raj/gxprc
gxpc explore --children_hard_limit 100 'basil[[100-199]]' 'basil[[200-220]]' 'basil[[300-320]]' 'basil[[400-420]]'

gxpc js -a work_file=$save_path/gxp_instructions  -a cpu_factor=0.6

rm -rf $save_path/src-shard.trans.merged
rm -rf $save_path/src-shard.trans.restored.merged
rm -rf $save_path/src-shard.trans.unk_replaced.merged
rm -rf $save_path/src-shard.trans.unk_replaced.restored.merged

for i in `seq -w 0 99999 | head -$num_shards`
do
	cat $save_path/src-shard-$i.trans >> $save_path/src-shard.trans.merged
	cat $save_path/src-shard-$i.trans.restored >> $save_path/src-shard.trans.restored.merged
	cat $save_path/src-shard-$i.trans.unk_replaced >> $save_path/src-shard.trans.unk_replaced.merged
	cat $save_path/src-shard-$i.trans.unk_replaced.restored >> $save_path/src-shard.trans.unk_replaced.restored.merged
done