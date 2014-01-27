#ifndef ENGINE_ALGORITHMSIMULATOR_H

#define ENGINE_ALGORITHMSIMULATOR_H
#include <vector>
#include <string>

namespace EasyQuant {
class TradingAlgorithm;
using std::vector;
using std::string;
    
/**
* @brief 
*/
class AlgorithmSimulator {
 public:
    AlgorithmSimulator(){ };
    void Run();
    void RegisterAlgorithm(TradingAlgorithm *algo, const string& fname);


 private:
    vector<TradingAlgorithm*>   algorithms_;
    
};

} /* EasyQuant */
#endif /* end of include guard: ENGINE_ALGORITHMSIMULATOR_H */
