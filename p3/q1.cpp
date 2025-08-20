#include <bits/stdc++.h>
#include <fstream>
using namespace std;
const int MOD=1e9+7;

class TrieNode{
    public:
    char curr;
    vector<TrieNode*>child;
    bool isend;
    int cnt;
     TrieNode(char val)
     {
        isend=false;
        cnt=0;
        child.resize(26,NULL);
        curr=val;
     }

};
class Trie{
    public:
    int tot;
    TrieNode* root;
    Trie()
    {
        tot=0;
        root=new TrieNode('\0');
    }

    void insert(string s)
    {
        tot++;
        TrieNode* curr=root;
        for(int i=0;i<s.length();i++)
        {
            TrieNode* next=NULL;
            if(curr->child[s[i]-'a']!=NULL)
            {
               next=curr->child[s[i]-'a'];
            }
            next=new TrieNode(s[i]);
            curr->child[s[i]-'a']=next;

            curr=next;
            curr->cnt++;
            if(i==s.length()-1)
            {
                curr->isend=true;
            }
        }
    }

    long double prob(string s)
    {
        TrieNode* curr=root;
        for(int i=0;i<s.length();i++)
        {
        TrieNode* next=NULL;
            if(curr->child[s[i]-'a']!=NULL)
            {
               next=curr->child[s[i]-'a'];
            }else{
                return 0;
            }
           
            if(i==s.length()-1)
            {
                return (curr->cnt)/tot;
            }
        }
    }



};

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
     std::string filename = "brown_nouns.txt"; // <-- Change this to your file's name

    // Create an input file stream object to read the file.
    std::ifstream inputFile(filename);

    // Always check if the file was opened successfully.
    if (!inputFile.is_open()) {
        std::cerr << "Error: Could not open file '" << filename << "'" << std::endl;
        return 1; // Exit with an error code
    }

    std::string word;
    // You could also store all words in a vector
    std::vector<std::string> allWords;

    // This loop reads from the file stream into the `word` string.
    // It will continue as long as there are words to read.
    Trie *tt=new Trie();
    while (inputFile >> word) {
        // Inside this loop, you have one word at a time.
        // You can now process it as needed.

        // Example 1: Print the word to the console.
        std::cout << "Read: " << word << std::endl;
          reverse(word.begin(),word.end());
          tt->insert(word);
        // Example 2: Add the word to a vector.
       

        // Example 3: Insert the word into your Trie (assuming you have a 'myTrie' object).
        // myTrie.insert(word);
    }
    cout<<tt->prob("se")<<"\n";
    cout<<tt->prob("s")<<"\n";

    // The file is automatically closed when `inputFile` goes out of scope.
    // But you can also close it manually if you want.
    inputFile.close();


}