/**
 * Created by jeff on 15/12/16.
 */
function pagerank_map(){
    var page = this;
    this.value.links.forEach(function(link){
        if(page.value.links.length > 0){
            emit(link, {
                pr: page.value.pr / page.value.links.length,
                links: []
            })
        }
    });
    emit(page._id, {
        pr: 1 / page.value.length,
        links: page.value.links,
        length: page.value.length
    })
}