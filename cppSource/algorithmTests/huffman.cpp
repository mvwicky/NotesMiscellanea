#include <iostream>
#include <queue>
#include <map>
#include <climits>
#include <iterator>
#include <algorithm>

const int UniqueSymbols << CHAR_BIT;
const char *SampleString = "this is an example for huffman encoding";

typedef std::vector<bool> HuffCode;
typedef std::map<char, HuffCode> HuffCodeMap;

class iNode {
public:
	const int f;
	virtual ~iNode();
protected:
	iNode(int f) : f{f} {}
};

class intNode : public iNode {
public:
	iNode *const left;
	iNode *const right;

	intNode(iNode *c0, iNode *c1) : iNode{c0->f + c1->f}, left{c0}, right{c1} {}
	~intNode(){
		delete left;
		delete right;
	}
};

class leafNode : public iNode {
public:
	const char c;

	leafNode(int f, char c) : iNode{f}, c{c} {}
};

struct nodeCmp {
	bool operator()(const iNode *lhs, const iNode *rhs) const {return lhs->f > rhs->f;}
};

iNode *buildTree(const int (&frequencies)[UniqueSymbols]){
	std::priority_queue<iNode*, std::vector<iNode*>, nodeCmp> trees;
	for (int i = 0; i < UniqueSymbols; i++){
		if (frequencies[i] != 0)
			trees.push(new leafNode(frequencies[i], char(i)));
	}
	while (trees.size() > 1){
		iNode *childR = trees.top();
		trees.pop();

		iNode *childL = trees.top();
		trees.pop();

		iNode *parent = new intNode(childR, childL);
		trees.push(parent);
	}
	return trees.top();
}

void generateCodes(const iNode *node, const HuffCode &prefix, HuffCodeMap &outCodes){
	if (const leafNode *lf = dynamic_cast<const leafNode*>(node))
		outCodes[lf->c] = prefix;
	else if (const intNode *in = dynamic_cast<const intNode*>(node)){
		HuffCode leftPrefix = prefix; 
		leftPrefix.push_back(false);
		generateCodes(in->left, leftPrefix, outCodes);

		HuffCode rightPrefix = prefix;
		rightPrefix.push_back(true);
		generateCodes(in->right, rightPrefix, outCodes);
	}
}

int main(){
	int frequencies[UniqueSymbols] = {0};
	const char *ptr = SampleString;
	while (*ptr != '\0')
		++frequencies[*ptr++];

	iNode *root = buildTree(frequencies);

	HuffCodeMap codes;
	generateCodes(root, HuffCode(), codes);
	delete root;

	for (HuffCodeMap::const_iterator it = codes.begin(); it != codes.end(); it++){
		std::cout << it->first << " ";
		std::copy(it->second.begin(), it->second().end(), std::ostream_iterator<bool>(std::cout));
		std::cout << std::endl;
	}
	return 0;
}