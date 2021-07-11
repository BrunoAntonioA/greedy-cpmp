
#include <map>
#include <vector>
#include <list>
#include <iterator>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include<ctime>
#include "dirent.h"

#include "Layout.h"
#include "Greedy.h"
#include "Bsg.h"

using namespace std;
using namespace cpmp;



int main(int argc, char * argv[]){

    Layout::H = atoi (argv[1]);
    Layout L;

    int carg=2;
    if(string(argv[carg++])== "--random") {
        srand(time(NULL));
        //cout << "Generating a random instance: S="<<argv[carg] << ", N="<<argv[carg+1] << ", H="<<Layout::H << endl;
        Layout::save_moves = true;
        L=Layout(atoi(argv[carg]), atoi(argv[carg+1]));
        //L.print();
        carg+=2;
    }else{
        L=Layout(argv[2]);
    }

    int beams = atoi (argv[carg++]);
    Layout best_lay = L;
    const clock_t begin_time = clock();
    int steps;
    //if (beams==0) steps = greedy_solve(L,1000);
    int type=ATOMIC_MOVE;
    bool PIXIE=true;
    if(argc>=carg+1 && string(argv[carg++])== "--FEG") PIXIE=false;
    if(argc>=carg+1 && string(argv[carg++])== "--compound_moves") type=SD_MOVE;
    
    
    
    if (beams==0){
        if(PIXIE) steps = pixie_solve(L,1000);
        else steps = greedy_solve(L,1000);
    }
    else steps = BSG(L, beams, type, best_lay, PIXIE);
    //cout << steps  << endl;

    int s=best_lay.moves.size();
    
    for(auto m : best_lay.moves){
        best_lay.move(m.second,m.first);
        //cout << "State-Action " << s-- << endl;
        best_lay.print();
        cout << "(" <<m.first <<"," << m.second << ")" << endl;
    }
    
    return 0;
}

