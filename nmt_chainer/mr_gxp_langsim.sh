save_path=$1
l1_file=$2
l2_file=$3
l1=$4
l2=$5
split_size=$6

rm -rf $save_path
mkdir -p $save_path
source /orange/brew/brew.sh
#split -a 3 -d -l 60 /windroot/raj/corpora_downloads/IWSLT2016/1s1t_ar_en/mlnmt.dev.tgt.raw $save_path/tgt-shard-
#split -a 3 -d -l 60 /windroot/raj/corpora_downloads/IWSLT2016/1s1t_ar_en/mlnmt.dev.src.raw $save_path/src-shard-

split -a 5 -d -l $split_size $l1_file $save_path/src-shard-
split -a 5 -d -l $split_size $l2_file $save_path/tgt-shard-

num_shards=`ls $save_path/src-shard-* | wc -l `
echo "Number of shards to be processed:" $num_shards

for i in `seq -w 0 99999 | head -$num_shards`
do
	echo "nice -n 19 bash /home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/mr_langsim.sh $save_path/src-shard-$i $save_path/tgt-shard-$i $l1 $l2 > $save_path/sim_score-$i"
done > $save_path/gxp_instructions

source /home/raj/gxprc
gxpc explore --children_hard_limit 100 'jungle' #'basil[[100-199]]' 'basil[[200-220]]' 'basil[[300-320]]' 'basil[[400-420]]'

gxpc js -a work_file=$save_path/gxp_instructions  -a cpu_factor=0.6

for i in `seq -w 0 99999 | head -$num_shards`
do
	cat $save_path/sim_score-$i >> $save_path/sim_score
	lines=`wc -l $save_path/src-shard-$i | cut -d ' ' -f1`
	echo "$lines" >> $save_path/num_lines
done

python /home/raj/softwares-and-scripts/NNProjects/knmt/nmt_chainer/calc_average.py $save_path/sim_score $save_path/num_lines > $save_path/sim_score_final

rm $save_path/sim_score-* $save_path/src-shard-* $save_path/tgt-shard-*