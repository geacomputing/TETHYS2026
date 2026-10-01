mkdir -p environments

for env in copernicusMarine ecmwf-datastores-client xarray; do
    conda run -n "$env" python -m pip freeze \
        > "environments/requirements_${env}.txt"

    conda env export -n "$env" --no-builds \
        | sed '/^prefix:/d' \
        > "environments/yml_${env}.yml"
done
