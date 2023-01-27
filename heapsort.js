var testList = [5, 223, 4213, 523, 543, 333, 2, 1, 9494, 33, 42, 33, 942];
var sortedList = []

const getLeftChild = (index) => 2 * index + 1;
const getRightChild = (index) => 2 * index + 2;
const getParent = (index) => {
  if (index === 0) {
    return undefined;
  }
  return Math.floor((index - 1) / 2);
}
const heapify = (index, list) => {
    var leftChild = getLeftChild(index);
    var rightChild = getRightChild(index);
    var largest = index;

    if(list[leftChild] > list[largest]) {
        largest = leftChild;
    }
    if (list[rightChild] > list[largest]) {
        largest = rightChild;
    }
    if (largest != index) {
        var temp = list[index];
        list[index] = list[largest];
        list[largest] = temp;
        return heapify(largest, list);
    }
    return list;
}

for (var i = getParent(testList.length - 1); i >= 0; i--) {
  testList = heapify(i, testList);
}

for (var i = 0; i < testList.length; i++) {
  const max = testList.shift()
  sortedList.unshift(max);
  heapify(0, testList)
}
console.log(sortedList);