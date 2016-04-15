/*
 *  Copyright 2002 California Institute of Technology
 */

#include "cantera/IdealGasMix.h"

using namespace std;
using namespace Cantera;

int main(int argc, char** argv)
{
#if defined(_MSC_VER) && _MSC_VER < 1900
    _set_output_format(_TWO_DIGIT_EXPONENT);
#endif
    try {
        IdealGasMix g("silane.xml", "silane");
        g.setState_TPX(1500.0, 100.0, "SIH4:0.01, H2:0.99");
        g.equilibrate("TP");
        return 0;
    } catch (CanteraError& err) {
        std::cerr << err.what() << std::endl;
        cerr << "program terminating." << endl;
        return -1;
    }
}
