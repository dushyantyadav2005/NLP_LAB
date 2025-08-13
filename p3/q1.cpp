#include <bits/stdc++.h>
using namespace std;
const int MOD=1e9+7;

class TrieNode{
    int curr;
    vector<TrieNode*>child;
     TrieNode(char val)
     {
        child.resize(26,NULL);
        curr=val-'a';
     }

};
class Trie{
    TrieNode* root;
    Trie()
    {
        root=new TrieNode(' ');
    }
}

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    

}