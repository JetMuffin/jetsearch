/**
 * Created by jeff on 15/12/16.
 */
function pagerank_map(){
    var page = this;
    this.value.links.forEach(function(link){
        emit(link, {
            pr: page.value.pr / page.value.links.length,
            links: []
        })
    });
    emit(page._id, {
        pr: page.value.pr,
        links: page.value.links
    })
}