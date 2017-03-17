source /orange/brew/brew.sh
totalgpus=0
totalgpusfree=0
for machinename in baracuda100 baracuda101 baracuda102 moss100 moss101 moss102 moss103 moss104 moss105
do
echo "Monitoring machine $machinename"
numgpus=`ssh $machinename nvidia-smi -L | wc -l`
totalgpus=`echo $totalgpus+$numgpus | bc`
numgpus=`echo $numgpus-1 | bc`
for i in `seq 0 $numgpus`      
do
runningprocesses=`ssh $machinename nvidia-smi -q -i $i | grep "Process ID" | wc -l`
if [[ $runningprocesses == "0" ]]
then
totalgpusfree=`echo $totalgpusfree+1 | bc`
prodtype=`ssh $machinename nvidia-smi -q -i $i | grep "Product Name" | cut -d ":" -f2`
echo "GPU with ID $i of type$prodtype is free"
else
procid=`ssh $machinename nvidia-smi -q -i $i | grep "Process ID" | cut -d ":" -f2 | cut -d ' ' -f2 | tail -1`
userid=`ssh $machinename ps aux | grep $procid | cut -d ' ' -f1 | tail -1`
prodtype=`ssh $machinename nvidia-smi -q -i $i | grep "Product Name" | cut -d ":" -f2`
echo "GPU with ID $i of type$prodtype is used by $userid"
fi
done
done
echo "Number of GPUs in stock: $totalgpus"
echo "Number of free GPUs: $totalgpusfree"