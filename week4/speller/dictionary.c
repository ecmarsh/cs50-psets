// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// Makes new node for trie inialized to NULL
node *make_node(void)
{
    node *new_node = malloc(sizeof(node));
    if (new_node == NULL)
    {
        return false;
    }

    new_node->is_word = false;
    for (int i = 0; i < N; i++)
    {
        new_node->children[i] = NULL;
    }

    return new_node;
}

int char_to_i(char c)
{
    // Allow only alphabetical characters and apostrophes
    if (c == '\'')
    {
        return (N - 1);
    }
    return (c - 'a');
}

// Intialize word counter
unsigned int words = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = make_node();

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word (& null character)
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        int length = strlen(word);
        int index, level;

        node *pCrawl = root;

        for (level = 0; level < length; level++)
        {
            index = char_to_i(word[level]);
            if (!pCrawl->children[index])
            {
                pCrawl->children[index] = make_node();
            }

            pCrawl = pCrawl->children[index];
        }

        // mark last node as leaf
        pCrawl->is_word = true;
        words++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index, level, length = strlen(word);
    node *pCrawl = root;

    // Go through word, level by level
    for (level = 0; level < length; level++)
    {
        index = (!isupper(word[level])) ? char_to_i(word[level]) : char_to_i(tolower(word[level]));
        if (!pCrawl->children[index])
        {
            return false;
        }

        pCrawl = pCrawl->children[index];
    }

    return (pCrawl != NULL && pCrawl->is_word);
}

void free_all(node *child)
{
    int i;
    // safe guard including root node.
    if (!child)
    {
        return; 
    }

    // Recursively free all children starting from bototm of tree
    for (i = 0; i < N; i++)
    {
        free_all(child->children[i]);
    }

    // base case
    free(child);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (root)
    {
        free_all(root);
        return true;
    }
    return false;
}
