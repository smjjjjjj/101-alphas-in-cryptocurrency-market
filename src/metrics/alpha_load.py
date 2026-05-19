import os
import importlib

def load_all_alphas(data, base_path="src/raw_alphas"):
    alpha_dict = {}

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.startswith("alpha") and file.endswith(".py"):
                
                # remove .py → alpha1
                module_name = file[:-3]

                # build module path: raw_alphas.momentum.alpha1
                rel_path = os.path.relpath(root, ".")
                module_path = rel_path.replace(os.sep, ".") + "." + module_name

                # import module
                module = importlib.import_module(module_path)

                # get function (same name as file)
                func = getattr(module, module_name)

                # extract alpha number (alpha1 → 1)
                alpha_id = int(module_name.replace("alpha", ""))

                # compute alpha
                alpha_dict[alpha_id] = func(data)

    return alpha_dict